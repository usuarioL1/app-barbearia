import unittest
from unittest.mock import AsyncMock, patch

from app_barbearia.mock_repository import MockFailure, MockRepository


class MockRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_mock_operations_never_call_the_http_client(self) -> None:
        with patch(
            "app_barbearia.api_client.request_json",
            new_callable=AsyncMock,
        ) as request:
            login = await MockRepository.authenticate(
                "lucas@email.com",
                "BarberFlow123!",
            )
            signup = await MockRepository.signup(
                name="Novo Cliente",
                email="novo@example.test",
                phone="11999999999",
                password="safe-demo-password",
            )
            appointment = await MockRepository.create_appointment(
                client_id="client-lucas",
                barber_id="rafael",
                service_id="corte",
                date="2026-08-25",
                start_time="09:45",
            )

        request.assert_not_awaited()
        self.assertEqual(login.data["role"], "client")
        self.assertEqual(signup.data["role"], "client")
        self.assertEqual(appointment.data["status"], "pending")
        for result in (login, signup, appointment):
            self.assertFalse(result.persisted)
            self.assertIn("simulada", result.message)
            self.assertIn("nada foi salvo", result.message)

    async def test_query_results_are_copies_of_the_mock_source(self) -> None:
        services = await MockRepository.services()
        services[0]["title"] = "Alterado localmente"

        fresh_services = await MockRepository.services()

        self.assertEqual(fresh_services[0]["title"], "Corte Masculino")

    async def test_service_catalog_contains_requested_services_and_preserves_existing(self) -> None:
        services = await MockRepository.services()
        by_title = {service["title"]: service for service in services}

        self.assertTrue(
            {
                "Corte Masculino",
                "Barba",
                "Combo",
                "Sobrancelha",
                "Pezinho / Acabamento",
                "Hidratação Capilar",
            }.issubset(by_title)
        )
        self.assertEqual(
            (by_title["Sobrancelha"]["duration_minutes"], by_title["Sobrancelha"]["price_cents"]),
            (15, 2000),
        )
        self.assertEqual(
            (
                by_title["Pezinho / Acabamento"]["duration_minutes"],
                by_title["Pezinho / Acabamento"]["price_cents"],
            ),
            (15, 1500),
        )
        self.assertEqual(
            (
                by_title["Hidratação Capilar"]["duration_minutes"],
                by_title["Hidratação Capilar"]["price_cents"],
            ),
            (30, 4000),
        )
        self.assertEqual(
            sum(service["title"] == "Sobrancelha" for service in services),
            1,
        )

    async def test_availability_respects_duration_and_preparation_interval(self) -> None:
        slots = await MockRepository.availability(
            "rafael",
            "corte",
            "2026-08-25",
        )

        self.assertNotIn("09:00", slots)
        self.assertIn("09:45", slots)
        self.assertIn("10:30", slots)

    async def test_unavailable_slot_returns_a_conflict_not_a_success(self) -> None:
        with self.assertRaises(MockFailure) as raised:
            await MockRepository.create_appointment(
                client_id="client-lucas",
                barber_id="rafael",
                service_id="corte",
                date="2026-08-25",
                start_time="09:00",
            )

        self.assertEqual(raised.exception.code, "appointment_conflict")
        self.assertEqual(raised.exception.status_code, 400)

    async def test_customer_appointments_are_scoped_to_the_requested_client(self) -> None:
        appointments = await MockRepository.customer_appointments("client-lucas")
        unrelated = await MockRepository.customer_appointments("client-matheus")

        self.assertTrue(appointments)
        self.assertTrue(all(item["client_id"] == "client-lucas" for item in appointments))
        self.assertTrue(unrelated)
        self.assertTrue(all(item["client_id"] == "client-matheus" for item in unrelated))

    async def test_cancellation_returns_a_non_persistent_copy(self) -> None:
        result = await MockRepository.cancel_appointment(
            "customer-upcoming-1",
            client_id="client-lucas",
        )
        original = await MockRepository.customer_appointments("client-lucas")

        self.assertEqual(result.data["status"], "cancelled")
        self.assertFalse(result.persisted)
        self.assertEqual(
            next(item for item in original if item["id"] == "customer-upcoming-1")[
                "status"
            ],
            "confirmed",
        )

    async def test_profile_update_returns_a_non_persistent_copy(self) -> None:
        result = await MockRepository.update_profile(
            "client-lucas",
            name="Lucas Atualizado",
            email="lucas-atualizado@example.test",
            phone="11911112222",
        )
        original = await MockRepository.user("client-lucas")

        self.assertEqual(result.data["name"], "Lucas Atualizado")
        self.assertFalse(result.persisted)
        self.assertEqual(original["name"], "Lucas Ferreira")

    async def test_reschedule_returns_a_non_persistent_copy(self) -> None:
        original = await MockRepository.appointment("customer-upcoming-1")
        result = await MockRepository.reschedule_appointment(
            "customer-upcoming-1",
            client_id="client-lucas",
            start_time="2026-08-25T11:45:00-03:00",
        )
        after = await MockRepository.appointment("customer-upcoming-1")

        self.assertEqual(result.data["date"], "2026-08-25")
        self.assertFalse(result.persisted)
        self.assertEqual(after["date"], original["date"])

    async def test_admin_appointment_filters_combine(self) -> None:
        appointments = await MockRepository.admin_appointments(
            barber_id="rafael",
            status="pending",
            date="2026-08-24",
        )

        self.assertEqual([item["id"] for item in appointments], ["barber-today-3"])

    async def test_barber_appointment_query_exposes_only_its_own_rows(self) -> None:
        appointments = await MockRepository.barber_appointments(
            "rafael",
            date="2026-08-24",
        )

        self.assertTrue(appointments)
        self.assertTrue(all(item["date"] == "2026-08-24" for item in appointments))
        self.assertNotIn("client_id", appointments[0])
        self.assertNotIn("client_email", appointments[0])

    async def test_barber_status_update_enforces_ownership_and_is_not_persistent(self) -> None:
        with self.assertRaises(MockFailure) as raised:
            await MockRepository.update_appointment_status(
                "customer-upcoming-2",
                "completed",
                actor_role="barber",
                barber_id="rafael",
            )

        self.assertEqual(raised.exception.status_code, 403)

        result = await MockRepository.update_appointment_status(
            "barber-today-3",
            "confirmed",
            actor_role="barber",
            barber_id="rafael",
        )
        original = await MockRepository.barber_appointments("rafael", date="2026-08-24")

        self.assertEqual(result.data["status"], "confirmed")
        self.assertFalse(result.persisted)
        self.assertEqual(
            next(item for item in original if item["id"] == "barber-today-3")[
                "status"
            ],
            "pending",
        )

    async def test_revenue_counts_only_completed_demo_appointments(self) -> None:
        monthly = await MockRepository.revenue("month", "2026-08-01")
        daily = await MockRepository.revenue("day", "2026-08-12")
        empty = await MockRepository.revenue("month", "2026-09-01")

        self.assertEqual(monthly, 11000)
        self.assertEqual(daily, 7000)
        self.assertEqual(empty, 0)

    async def test_admin_mutation_is_validated_and_not_persisted(self) -> None:
        result = await MockRepository.admin_mutation(
            "service",
            "create",
            {"title": "Serviço", "price": "40,00", "duration": "30"},
        )

        self.assertFalse(result.persisted)
        self.assertIn("nada foi salvo", result.message)
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "service",
                "create",
                {"title": "Serviço", "price": "0", "duration": "30"},
            )
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "service",
                "create",
                {"title": "", "price": "40", "duration": "30"},
            )
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "service",
                "create",
                {"title": "Serviço", "price": "40", "duration": "0"},
            )
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "service",
                "update",
                {
                    "id": "corte",
                    "title": "Serviço",
                    "price": "40",
                    "duration": "inválido",
                },
            )

    async def test_admin_client_create_and_update_validate_phone_without_persisting(
        self,
    ) -> None:
        create = await MockRepository.admin_mutation(
            "client",
            "create",
            {"name": "Novo Cliente", "phone": "(11) 99999-0000"},
        )
        update = await MockRepository.admin_mutation(
            "client",
            "update",
            {
                "id": "client-joao",
                "name": "João Silva",
                "phone": "(11) 98765-4321",
            },
        )
        self.assertFalse(create.persisted)
        self.assertFalse(update.persisted)
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "client",
                "update",
                {
                    "id": "client-joao",
                    "name": "João Silva",
                    "phone": "123",
                },
            )

    async def test_admin_barber_mutations_require_name_and_specialty(self) -> None:
        result = await MockRepository.admin_mutation(
            "barber",
            "create",
            {"name": "Novo Barbeiro", "specialty": "Corte"},
        )

        self.assertFalse(result.persisted)
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "barber",
                "create",
                {"name": "Novo Barbeiro", "specialty": ""},
            )
        with self.assertRaises(MockFailure):
            await MockRepository.admin_mutation(
                "barber",
                "update",
                {
                    "id": "rafael",
                    "name": "",
                    "specialty": "Corte",
                },
            )

    async def test_public_signup_cannot_choose_a_privileged_role(self) -> None:
        result = await MockRepository.signup(
            name="Novo Cliente",
            email="novo@example.test",
            phone="11999999999",
            password="safe-demo-password",
        )

        self.assertEqual(result.data["role"], "client")
        self.assertFalse(result.persisted)


if __name__ == "__main__":
    unittest.main()
