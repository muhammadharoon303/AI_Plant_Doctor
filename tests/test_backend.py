import unittest
import io
import sys
import os
import uuid
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from fastapi.testclient import TestClient
from app.main import app

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"], "AI Plant Doctor")

    def test_diseases_endpoint(self):
        response = self.client.get("/api/v1/diseases?lang=ur")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertGreater(len(data["items"]), 0)

    def test_assistant_endpoint(self):
        response = self.client.post("/api/v1/assistant", json={"message": "blight disease", "language": "en"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("blight", response.json()["response"].lower())

    def test_auth_flow(self):
        unique_email = f"farmer_{uuid.uuid4().hex[:6]}@example.com"
        password = "SecurePassword123"

        # 1. Register User
        reg_response = self.client.post(
            "/api/v1/auth/register",
            json={"email": unique_email, "password": password, "full_name": "Test Farmer", "language_preference": "ur"}
        )
        self.assertEqual(reg_response.status_code, 201)
        self.assertEqual(reg_response.json()["email"], unique_email)

        # 2. Login User
        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"email": unique_email, "password": password}
        )
        self.assertEqual(login_response.status_code, 200)
        token_data = login_response.json()
        self.assertIn("access_token", token_data)

        # 3. Read /me with Bearer token
        token = token_data["access_token"]
        me_response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()["email"], unique_email)

        # 4. Forgot Password
        forgot_response = self.client.post(
            "/api/v1/auth/forgot-password",
            json={"email": unique_email}
        )
        self.assertEqual(forgot_response.status_code, 200)
        self.assertIn("message", forgot_response.json())

    def test_plant_crud_flow(self):
        # 1. Register & Login
        email = f"farmer_{uuid.uuid4().hex[:6]}@example.com"
        self.client.post("/api/v1/auth/register", json={"email": email, "password": "pass"})
        login_res = self.client.post("/api/v1/auth/login", json={"email": email, "password": "pass"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create Plant
        create_res = self.client.post(
            "/api/plants",
            headers=headers,
            json={"name": "Greenhouse Row 4", "crop_type": "Tomato", "variety": "Cherry", "location": "Field A", "notes": "Fertilized weekly"}
        )
        self.assertEqual(create_res.status_code, 201)
        plant_data = create_res.json()
        plant_id = plant_data["id"]
        self.assertEqual(plant_data["name"], "Greenhouse Row 4")
        self.assertEqual(plant_data["location"], "Field A")

        # 3. List Plants
        list_res = self.client.get("/api/plants", headers=headers)
        self.assertEqual(list_res.status_code, 200)
        self.assertGreater(len(list_res.json()), 0)

        # 4. Get Plant Details
        get_res = self.client.get(f"/api/plants/{plant_id}", headers=headers)
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], plant_id)

        # 5. Update Plant
        put_res = self.client.put(
            f"/api/plants/{plant_id}",
            headers=headers,
            json={"name": "Updated Greenhouse Row 4", "location": "Field B"}
        )
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.json()["name"], "Updated Greenhouse Row 4")

        # 6. Get Plant Scans Timeline & Progress
        scans_res = self.client.get(f"/api/plants/{plant_id}/scans", headers=headers)
        self.assertEqual(scans_res.status_code, 200)
        self.assertIn("items", scans_res.json())

        progress_res = self.client.get(f"/api/plants/{plant_id}/progress", headers=headers)
        self.assertEqual(progress_res.status_code, 200)
        self.assertIn("health_trend", progress_res.json())
        self.assertIn("disease_history", progress_res.json())

        # 7. Delete Plant
        del_res = self.client.delete(f"/api/plants/{plant_id}", headers=headers)
        self.assertEqual(del_res.status_code, 204)

    def test_diagnosis_analyze_endpoint(self):
        # Create synthetic valid green leaf image
        img = Image.new("RGB", (300, 300), color=(40, 180, 50))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        files = {"file": ("test_leaf.jpg", buf, "image/jpeg")}
        data = {"lang": "en"}

        response = self.client.post("/api/diagnosis/analyze", files=files, data=data)
        self.assertEqual(response.status_code, 200)
        res_data = response.json()
        self.assertIn("scan_id", res_data)
        self.assertIn("crop", res_data)
        self.assertIn("disease", res_data)
        self.assertIn("confidence", res_data)
        self.assertIn("model_version", res_data)
        self.assertIn("image_url", res_data)

    def test_agricultural_knowledge_base(self):
        response = self.client.get("/api/v1/diseases?lang=en")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertGreater(data["total"], 0)

        disease_item = data["items"][0]
        self.assertIn("region", disease_item)
        self.assertIn("review_date", disease_item)
        self.assertIn("sources", disease_item)
        self.assertGreater(len(disease_item["sources"]), 0)

        loc_info = disease_item["localized_info"]
        self.assertIn("symptoms", loc_info)
        self.assertIn("causes", loc_info)
        self.assertIn("risk_factors", loc_info)
        self.assertIn("management", loc_info)
        self.assertIn("biological_treatment", loc_info)
        self.assertIn("chemical_treatment", loc_info)
        self.assertIn("prevention", loc_info)
        self.assertIn("safety_information", loc_info)

    def test_diagnosis_history_endpoints(self):
        # 1. Fetch History List
        history_res = self.client.get("/api/diagnosis/history?q=Tomato")
        self.assertEqual(history_res.status_code, 200)
        history_data = history_res.json()
        self.assertIn("items", history_data)
        self.assertIn("total", history_data)

        if history_data["total"] > 0:
            item = history_data["items"][0]
            self.assertIn("scan_id", item)
            self.assertIn("crop", item)
            self.assertIn("disease", item)
            self.assertIn("confidence", item)
            self.assertIn("model_version", item)
            self.assertIn("segmentation_status", item)
            self.assertIn("affected_percentage", item)
            self.assertIn("severity_stage", item)
            self.assertIn("created_at", item)

            # 2. Fetch History Item Detail by ID
            scan_id = item["scan_id"]
            detail_res = self.client.get(f"/api/diagnosis/{scan_id}")
            self.assertEqual(detail_res.status_code, 200)
            detail_data = detail_res.json()
            self.assertEqual(detail_data["scan_id"], scan_id)

    def test_notifications_and_low_confidence_safeguard(self):
        # 1. Register User & Auth Headers
        self.client.post(
            "/api/v1/auth/register",
            json={"email": "notif_user@example.com", "password": "securepassword123", "full_name": "Farmer John"}
        )
        login_res = self.client.post(
            "/api/v1/auth/login",
            json={"email": "notif_user@example.com", "password": "securepassword123"}
        )
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Test Get Notification Settings
        settings_res = self.client.get("/api/v1/notifications/settings", headers=headers)
        self.assertEqual(settings_res.status_code, 200)
        self.assertTrue(settings_res.json()["notifications_enabled"])

        # 3. Test Update Notification Settings (quiet hours, frequency)
        update_res = self.client.put(
            "/api/v1/notifications/settings",
            headers=headers,
            json={"reminder_frequency": "daily", "quiet_hours_enabled": True, "quiet_hours_start": "23:00", "quiet_hours_end": "06:00"}
        )
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.json()["reminder_frequency"], "daily")
        self.assertTrue(update_res.json()["quiet_hours_enabled"])

        # 4. Test Low Confidence Safeguard (Ensures non-alarming notification created)
        from app.services.notification_service import NotificationService
        from database.models.user import User
        from app.core.database import SessionLocal
        with SessionLocal() as db_session:
            user = db_session.query(User).filter_by(email="notif_user@example.com").first()
            if user:
                notif = NotificationService.process_scan_monitoring_trigger(
                    db=db_session,
                    user_id=user.id,
                    plant_name="Tomato Row A",
                    health_trend="Stable",
                    confidence=0.45 # Low confidence (45%)
                )
                self.assertIsNotNone(notif)
                self.assertEqual(notif.type, "low_confidence_reminder")

    def test_ai_assistant_rag_pipeline_and_safety_guard(self):
        # 1. Ask general disease explanation question
        res1 = self.client.post(
            "/api/v1/assistant",
            json={"message": "Why is my tomato plant showing these spots?", "language": "en"}
        )
        self.assertEqual(res1.status_code, 200)
        data1 = res1.json()
        self.assertIn("response", data1)
        self.assertIn("disclaimer", data1)

        # 2. Ask unverified dosage question -> Triggers Safety Guard
        res2 = self.client.post(
            "/api/v1/assistant",
            json={"message": "What is the exact grams per liter pesticide dose?", "language": "en"}
        )
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()
        self.assertIn("cannot independently invent chemical pesticide dosages", data2["response"])

    def test_multilingual_knowledge_and_safety_preservation(self):
        # 1. Fetch Urdu Knowledge Base
        res_ur = self.client.get("/api/v1/diseases?lang=ur")
        self.assertEqual(res_ur.status_code, 200)
        data_ur = res_ur.json()["items"][0]
        # Verify scientific name remains unchanged
        self.assertIn("scientific_name", data_ur)
        self.assertTrue(len(data_ur["scientific_name"]) > 0)
        self.assertIn("localized_info", data_ur)
        self.assertTrue(len(data_ur["localized_info"]["name"]) > 0)

        # 2. Fetch Pashto Knowledge Base
        res_ps = self.client.get("/api/v1/diseases?lang=ps")
        self.assertEqual(res_ps.status_code, 200)
        data_ps = res_ps.json()["items"][0]
        self.assertIn("localized_info", data_ps)
        self.assertTrue(len(data_ps["localized_info"]["name"]) > 0)

    def test_admin_dashboard_endpoints_and_role_security(self):
        # 1. Register Admin User
        admin_email = f"admin_{uuid.uuid4().hex[:6]}@plantdoctor.ai"
        self.client.post("/api/v1/auth/register", json={"email": admin_email, "password": "AdminPassword123"})
        
        from database.models.user import User
        from app.core.database import SessionLocal
        with SessionLocal() as db_session:
            u = db_session.query(User).filter_by(email=admin_email).first()
            if u:
                u.is_admin = True
                db_session.commit()

        # 2. Login as Admin
        login_res = self.client.post("/api/v1/auth/login", json={"email": admin_email, "password": "AdminPassword123"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Test GET /api/v1/admin/metrics
        metrics_res = self.client.get("/api/v1/admin/metrics", headers=headers)
        self.assertEqual(metrics_res.status_code, 200)
        m_data = metrics_res.json()
        self.assertIn("total_users", m_data)
        self.assertIn("total_scans", m_data)
        self.assertIn("low_confidence_rate", m_data)
        self.assertIn("active_model_version", m_data)

        # 4. Test GET /api/v1/admin/models
        models_res = self.client.get("/api/v1/admin/models", headers=headers)
        self.assertEqual(models_res.status_code, 200)
        self.assertIn("accuracy", models_res.json())

        # 5. Test Non-Admin Role Security (403 Forbidden)
        user_email = f"regular_{uuid.uuid4().hex[:6]}@example.com"
        self.client.post("/api/v1/auth/register", json={"email": user_email, "password": "RegularPassword123"})
        reg_login = self.client.post("/api/v1/auth/login", json={"email": user_email, "password": "RegularPassword123"})
        reg_headers = {"Authorization": f"Bearer {reg_login.json()['access_token']}"}

        forbidden_res = self.client.get("/api/v1/admin/metrics", headers=reg_headers)
        self.assertEqual(forbidden_res.status_code, 403)

if __name__ == "__main__":
    unittest.main()
