"""
Seed script to populate multi-lingual Disease Knowledge Base for English, Urdu, and Pashto.
"""

INITIAL_DISEASES = [
    {
        "disease_key": "Tomato___Early_blight",
        "crop_name": "Tomato",
        "scientific_name": "Alternaria solani",
        "category": "Fungal",
        "translations": {
            "en": {
                "name": "Tomato Early Blight",
                "description": "A common fungal disease affecting tomato leaves, stems, and fruit, characterized by concentric dark spots.",
                "symptoms": "Concentric dark brown to black rings on older leaves, yellowing around spots, defoliation.",
                "biological_treatment": "Apply Neem oil (0.5%), bio-fungicides containing Bacillus subtilis, and crop rotation.",
                "chemical_treatment": "Apply Copper-based fungicides or Chlorothalonil every 7-10 days upon first symptom appearance.",
                "prevention": "Ensure wide plant spacing for airflow, avoid overhead watering, and mulch lower leaves."
            },
            "ur": {
                "name": "ٹماٹر کا زراعت اگیتا جھلسائو (Early Blight)",
                "description": "ٹماٹر کے پتوں اور تنے کی عام پھپھوندی کی بیماری جس میں پتے پر کالے دائرے بنتے ہیں۔",
                "symptoms": "پرانے پتوں پر بھورے اور کالے دائرے، پتوں کا پیلا پڑنا اور گرنا۔",
                "biological_treatment": "نیم کے تیل کا اسپرے کریں اور فصلوں میں ردوبدل کا طریقہ اپنائیں۔",
                "chemical_treatment": "کاپر فنگی سائیڈ یا کلوروتھالونل کا 7 سے 10 دن کے وقفے سے اسپرے کریں۔",
                "prevention": "پودوں میں مناسب فاصلہ رکھیں اور پتوں پر براہ راست پانی دینے سے گریز کریں۔"
            },
            "ps": {
                "name": "د رومیانو وخته سوځېدنه (Early Blight)",
                "description": "د رومیانو یو عام فنګسي ناروغي ده چې پر پاڼو او ډنډرونو تورې حلقې جوړوي.",
                "symptoms": "په زړو پاڼو تورې او نسواري حلقې، د پاڼو ژېړېدل او توېدل.",
                "biological_treatment": "د نیم تېل او بایو فنګسي سایډ وکاروئ.",
                "chemical_treatment": "د مسو (Copper) محلول یا کلوروتالونیل درمل سپری کړئ.",
                "prevention": "د بوټو ترمینځ فاصله وساتئ او له پورته څخه اوبه مه ورکوئ."
            }
        }
    },
    {
        "disease_key": "Potato___Late_blight",
        "crop_name": "Potato",
        "scientific_name": "Phytophthora infestans",
        "category": "Oomycete",
        "translations": {
            "en": {
                "name": "Potato Late Blight",
                "description": "A destructive water-mold disease that rapidly destroys potato foliage and tubers.",
                "symptoms": "Water-soaked dark green to purple lesions on leaves, white fungal growth on leaf undersides in humid weather.",
                "biological_treatment": "Use resistant varieties, apply Trichoderma viride bio-agent.",
                "chemical_treatment": "Apply systemic fungicides containing Metalaxyl, Mancozeb, or Cymoxanil.",
                "prevention": "Plant certified disease-free tubers and ensure well-drained soil."
            },
            "ur": {
                "name": "آلو کا پچھیتا جھلسائو (Late Blight)",
                "description": "آلو کی فصل کو تیزی سے تباہ کرنے والی خطرناک بیماری۔",
                "symptoms": "پتوں پر گہرے سبز اور ارغوانی داغ، پتوں کے نچلے حصے پر سفید پھپھوندی۔",
                "biological_treatment": "ٹرائیکوڈرما بائیو ایجنٹ اور بیماری سے محفوظ بیج استعمال کریں۔",
                "chemical_treatment": "مینکوزیب (Mancozeb) یا میٹالیکسل کا فوری اسپرے کریں۔",
                "prevention": "صرف تصدیق شدہ بیج بوئیں اور کھیت میں پانی جمع نہ ہونے دیں۔"
            },
            "ps": {
                "name": "د کچالو ناوخته سوځېدنه (Late Blight)",
                "description": "د کچالو د فصل یوه ډېره خطرناکه او اوبه لرونکې فنګسي ناروغي.",
                "symptoms": "پر پاڼو تاره او ارغواني داغونه او لاندې خوا ته سپینه پپوندک.",
                "biological_treatment": "د ناروغۍ مقاومت لرونکي بیجونه او ټراېکوډرما وکاروئ.",
                "chemical_treatment": "د مانکوزیب او میټالکسل کیمیاوي درمل سپری کړئ.",
                "prevention": "روغ او تایید شوي کچالو وکرئ او د اوبو د درېدو مخنیوی وکړئ."
            }
        }
    },
    {
        "disease_key": "Tomato___healthy",
        "crop_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "Healthy",
        "translations": {
            "en": {
                "name": "Healthy Tomato Leaf",
                "description": "The plant foliage appears healthy with rich green leaf color and no visible disease symptoms.",
                "symptoms": "None. Leaf is vibrant and healthy.",
                "biological_treatment": "Maintain balanced organic fertilization and regular monitoring.",
                "chemical_treatment": "No chemical treatment required.",
                "prevention": "Continue standard crop management practices."
            },
            "ur": {
                "name": "صحت مند ٹماٹر کا پودا",
                "description": "پودا بالکل صحت مند ہے، پتوں کا رنگ گہرا سبز اور کسی بیماری کے اثرات نہیں ہیں۔",
                "symptoms": "کوئی علامات نہیں، پتا تروتازہ ہے۔",
                "biological_treatment": "نامیاتی کھاد کا متوازن استعمال جاری رکھیں۔",
                "chemical_treatment": "کسی کیمیائی اسپرے کی ضرورت نہیں ہے۔",
                "prevention": "معمول کے مطابق دیکھ بھال جاری رکھیں۔"
            },
            "ps": {
                "name": "روغ درومیانو بوټی",
                "description": "بوټی بشپړ روغ دی او هیڅ ډول د ناروغۍ نښې نلري.",
                "symptoms": "هیڅ نښې نشته، پاڼه تازه ده.",
                "biological_treatment": "د متوازنې عضوي سرې کارول جاري وساتئ.",
                "chemical_treatment": "کیمیاوي درملو ته اړتیا نشته.",
                "prevention": "د بوټي پاملرنې ته دوام ورکړئ."
            }
        }
    }
]

def seed_diseases(db_session):
    from database.models.disease import Disease
    for item in INITIAL_DISEASES:
        existing = db_session.query(Disease).filter_by(disease_key=item["disease_key"]).first()
        if not existing:
            disease = Disease(
                disease_key=item["disease_key"],
                crop_name=item["crop_name"],
                scientific_name=item["scientific_name"],
                category=item["category"],
                translations=item["translations"]
            )
            db_session.add(disease)
    db_session.commit()
    print(f"[Seed] Successfully seeded {len(INITIAL_DISEASES)} multi-lingual diseases.")
