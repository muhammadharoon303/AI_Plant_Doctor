"""
Comprehensive Seed script for Multi-Crop Universal Disease Knowledge Base with Exact Dosages.
Supports English, Urdu, and Pashto.
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
                "description": "A fungal disease affecting tomato leaves, stems, and fruit with concentric dark spots.",
                "symptoms": "Concentric dark brown to black rings on older leaves, yellow halo surrounding spots, defoliation.",
                "biological_treatment": "Dosage: Spray Neem Oil (0.5% concentration, 5ml per Liter of water) or Bacillus subtilis (3g per Liter water) every 7 days.",
                "chemical_treatment": "Dosage: Spray Copper Oxychloride 50% WP at 2.5g per Liter water OR Mancozeb 75% WP at 2.0g per Liter water every 7-10 days. Pre-Harvest Interval (PHI): 7 days.",
                "prevention": "Maintain 60cm plant spacing, apply straw mulch, avoid overhead sprinkler irrigation."
            },
            "ur": {
                "name": "ٹماٹر کا اگیتا جھلسائو (Early Blight)",
                "description": "ٹماٹر کی پھپھوندی کی بیماری جس میں پتوں پر گول گہرے چھلے بنتے ہیں۔",
                "symptoms": "پرانے پتوں پر گہرے بھورے چھلے، پتوں کا پیلا ہونا اور جھڑنا۔",
                "biological_treatment": "خوراک: نیم کا تیل 5 ملی لیٹر فی لیٹر پانی یا باسیلس سبٹیلس 3 گرام فی لیٹر پانی 7 دن کے وقفے سے اسپرے کریں۔",
                "chemical_treatment": "خوراک: کاپر آکسی کلورائڈ 2.5 گرام فی لیٹر پانی یا مینکوزیب 2 گرام فی لیٹر پانی کا اسپرے کریں۔ پھل توڑنے سے 7 دن پہلے اسپرے روک دیں۔",
                "prevention": "پودوں میں 60 سینٹی میٹر فاصلہ رکھیں اور پتوں پر براہ راست پانی نہ ڈالیں۔"
            },
            "ps": {
                "name": "د رومیانو وخته سوځېدنه (Early Blight)",
                "description": "د رومیانو عام فنګسي ناروغي ده چې پر پاڼو تورې حلقې جوړوي.",
                "symptoms": "په زړو پاڼو تورې او نسواري حلقې، د پاڼو ژېړېدل او توېدل.",
                "biological_treatment": "اندازه: د نیم تېل 5 ملی لیتر په 1 لیتر اوبو کې ګډ کړئ او په هره اونۍ کې سپری کړئ.",
                "chemical_treatment": "اندازه: کاپر آکسی کلورایډ 2.5 ګرامه په 1 لیتر اوبو کې یا مانکوزیب 2 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "د بوټو ترمنځ فاصله وساتئ او له پورته اوبه مه ورکولوئ."
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
                "description": "A destructive water-mold disease that rapidly causes foliage decay and tuber rot.",
                "symptoms": "Water-soaked dark green to purple spots on leaves, white downy mildew under leaf surfaces during cool humid weather.",
                "biological_treatment": "Dosage: Apply Trichoderma viride bio-agent (5g per Liter water) or copper sulfate soap spray.",
                "chemical_treatment": "Dosage: Spray Metalaxyl + Mancozeb (2.5g per Liter water) or Cymoxanil 8% + Mancozeb 64% at 2.0g per Liter water at first warning. PHI: 14 days.",
                "prevention": "Plant certified disease-free tubers, hill soil over developing tubers, ensure field drainage."
            },
            "ur": {
                "name": "آلو کا پچھیتا جھلسائو (Late Blight)",
                "description": "آلو کے پتوں اور آلو کے دانے کو تیزی سے تباہ کرنے والی مائلڈ بیماری۔",
                "symptoms": "پتوں پر ارغوانی اور سیاہ پانی زدہ دھبے، پتوں کی نچلی سطح پر سفید پھپھوندی۔",
                "biological_treatment": "خوراک: ٹرائیکوڈرما وائرڈے 5 گرام فی لیٹر پانی ملا کر اسپرے کریں۔",
                "chemical_treatment": "خوراک: میٹالیکسل + مینکوزیب 2.5 گرام فی لیٹر پانی ملا کر 8 سے 10 دن کے وقفے سے اسپرے کریں۔",
                "prevention": "صرف تصدیق شدہ بیج بوئیں اور کھیت میں پانی جمع نہ ہونے دیں۔"
            },
            "ps": {
                "name": "د کچالو ناوخته سوځېدنه (Late Blight)",
                "description": "د کچالو تر ټولو خطرناکه فنګسي ناروغي ده.",
                "symptoms": "پر پاڼو تاره او ارغواني داغونه او لاندې سپینه پپوندک.",
                "biological_treatment": "اندازه: ټرایکوډرما بایو ایجنټ 5 ګرامه په 1 لیتر اوبو کې وکاروئ.",
                "chemical_treatment": "اندازه: میټالکسل + مانکوزیب 2.5 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "د تایید شویو بیجونو څخه استفاده وکړئ."
            }
        }
    },
    {
        "disease_key": "Apple___Apple_scab",
        "crop_name": "Apple",
        "scientific_name": "Venturia inaequalis",
        "category": "Fungal",
        "translations": {
            "en": {
                "name": "Apple Scab",
                "description": "Fungal infection causing olive-green to black velvety spots on apple leaves and fruit.",
                "symptoms": "Olive-green lesions turning dark brown/black on leaf surfaces, scabbed corky fruit spots.",
                "biological_treatment": "Dosage: Apply Sulfur WP 80% at 3g per Liter water OR Potassium Bicarbonate at 4g per Liter water.",
                "chemical_treatment": "Dosage: Apply Captan 50% WP (2.5g per Liter water) or Difenoconazole 25% EC (0.5ml per Liter water). PHI: 14 days.",
                "prevention": "Rake and burn fallen orchard leaves in autumn, prune tree canopy for maximum sunlight."
            },
            "ur": {
                "name": "سیب کا اسکیب (Apple Scab)",
                "description": "سیب کے پتوں اور پھل پر زیتونی اور سیاہ داغ پیدا کرنے والی بیماری۔",
                "symptoms": "پتوں پر زیتونی سیاہ دھبے اور پھل کی سکن کا سخت ہو کر پھٹنا۔",
                "biological_treatment": "خوراک: سلفر 80% 3 گرام فی لیٹر پانی ملا کر اسپرے کریں۔",
                "chemical_treatment": "خوراک: کیپٹان 2.5 گرام فی لیٹر پانی یا ڈیفینوکونازول 0.5 ملی لیٹر فی لیٹر پانی اسپرے کریں۔",
                "prevention": "گرے ہوئے پرانے پتوں کو تلف کریں اور درخت کی چھٹائی کریں۔"
            },
            "ps": {
                "name": "د مڼې سکېب (Apple Scab)",
                "description": "د مڼو په پاڼو او میوو تور داغونه جوړوي.",
                "symptoms": "په پاڼو او میوه تاره او زیتوني ټکي.",
                "biological_treatment": "اندازه: سلفر 3 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "chemical_treatment": "اندازه: کاپټان 2.5 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "زاړه توېدلي پاڼې وسوزوئ."
            }
        }
    },
    {
        "disease_key": "Corn_(maize)___Northern_Leaf_Blight",
        "crop_name": "Corn (Maize)",
        "scientific_name": "Exserohilum turcicum",
        "category": "Fungal",
        "translations": {
            "en": {
                "name": "Corn Northern Leaf Blight",
                "description": "Fungal leaf disease causing elongated cigar-shaped lesions on maize foliage.",
                "symptoms": "Long grayish-green to tan cigar-shaped spots (2-15 cm long) on leaves.",
                "biological_treatment": "Dosage: Spray Pseudomonas fluorescens (5g per Liter water) and practice crop rotation.",
                "chemical_treatment": "Dosage: Apply Azoxystrobin 23% SC at 1.0ml per Liter water OR Propiconazole 25% EC at 1.0ml per Liter water. PHI: 21 days.",
                "prevention": "Plant resistant maize hybrids, plow under infected crop residue after harvest."
            },
            "ur": {
                "name": "مکئی کا شمالی پتا جھلسائو (Northern Leaf Blight)",
                "description": "مکئی کے پتوں پر لمبے سگار کی شکل کے داغ بنانے والی بیماری۔",
                "symptoms": "پتوں پر 2 سے 15 سینٹی میٹر لمبے گہرے سرمئی اور بھورے داغ۔",
                "biological_treatment": "خوراک: سوڈوموناس فلوروسینس 5 گرام فی لیٹر پانی ملائیں اور اسپرے کریں۔",
                "chemical_treatment": "خوراک: ایزوکسیسٹروبن 1 ملی لیٹر فی لیٹر پانی یا پروپیکونازول 1 ملی لیٹر فی لیٹر پانی اسپرے کریں۔",
                "prevention": "بیماری سے پاک ہائبرڈ بیج استعمال کریں اور فصل کے بچے حصے تلف کریں۔"
            },
            "ps": {
                "name": "د جوارو د پاڼو سوځېدنه (Northern Leaf Blight)",
                "description": "د جوارو په پاڼو اوږده سګرټ بڼه داغونه جوړوي.",
                "symptoms": "په پاڼو اوږده خړ او نسواري داغونه.",
                "biological_treatment": "اندازه: سیوډوموناس 5 ګرامه په 1 لیتر اوبو کې ګډ کړئ.",
                "chemical_treatment": "اندازه: پروپیکونازول 1 ملي لیتر په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "مقاوم هائبرډ تخم وکرئ."
            }
        }
    },
    {
        "disease_key": "Grape___Black_rot",
        "crop_name": "Grape",
        "scientific_name": "Guignardia bidwellii",
        "category": "Fungal",
        "translations": {
            "en": {
                "name": "Grape Black Rot",
                "description": "Fungal disease causing reddish-brown leaf spots and shriveled black mummified berries.",
                "symptoms": "Small reddish-brown circular spots on leaves, fruit turns black, shrivels into hard mummies.",
                "biological_treatment": "Dosage: Apply Copper Hydroxide (2.0g per Liter water) or Serenade ASO (Bacillus subtilis, 4ml/L).",
                "chemical_treatment": "Dosage: Spray Myclobutanil 10% WP (0.4g per Liter water) or Mancozeb (2.0g per Liter water). PHI: 14 days.",
                "prevention": "Prune mummified fruit clusters during winter dormancy, maintain vine trellis air movement."
            },
            "ur": {
                "name": "انگور کا بلیک راٹ (Black Rot)",
                "description": "انگور کے دانوں اور پتوں کا سیاہ اور سوکھ کر سخت ہو جانا۔",
                "symptoms": "پتوں پر سرخ بھورے دھبے، انگور کے دانے سیاہ اور سوکھ کر ممی بن جاتے ہیں۔",
                "biological_treatment": "خوراک: کاپر ہائیڈرو آکسائیڈ 2 گرام فی لیٹر پانی میں اسپرے کریں۔",
                "chemical_treatment": "خوراک: مائیکلوبوٹانل 0.4 گرام فی لیٹر پانی یا مینکوزیب 2 گرام فی لیٹر پانی اسپرے کریں۔",
                "prevention": "سردیوں میں پرانے سوکھے انگور تلف کریں اور بیلوں کی چھٹائی کریں۔"
            },
            "ps": {
                "name": "د انګورو تور خوساوالی (Black Rot)",
                "description": "د انګورو دانې وچې او تورې کوي.",
                "symptoms": "په پاڼو نسواري ټکي او د انګورو دانې تورېدل.",
                "biological_treatment": "اندازه: کاپر هایډروکسایډ 2 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "chemical_treatment": "اندازه: مانکوزیب 2 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "د انګورو واښه او مړه دانې پرې کړئ."
            }
        }
    },
    {
        "disease_key": "Pepper,_bell___Bacterial_spot",
        "crop_name": "Pepper (Bell)",
        "scientific_name": "Xanthomonas euvesicatoria",
        "category": "Bacterial",
        "translations": {
            "en": {
                "name": "Pepper Bacterial Spot",
                "description": "Bacterial infection affecting pepper foliage and fruit causing dark water-soaked spots.",
                "symptoms": "Small yellow-green leaf lesions turning dark brown with raised margins, leaf drop.",
                "biological_treatment": "Dosage: Spray Copper Hydroxide + Mancozeb tank mix or Streptomyces lydicus bio-fungicide.",
                "chemical_treatment": "Dosage: Spray Fixed Copper (2.5g per Liter water) mixed with Mancozeb (2.0g per Liter water) every 7 days.",
                "prevention": "Use pathogen-free seed, soak seeds in hot water (50°C for 25 mins) before planting."
            },
            "ur": {
                "name": "شملہ مرچ کا بیکٹیریل اسپاٹ",
                "description": "مرچ کے پتوں اور پھل پر بیکٹیریا کے گہرے داغ۔",
                "symptoms": "پتوں پر چھوٹے سبز پیلے داغ جو بعد میں گہرے بھورے ہو جاتے ہیں اور پتے گرتے ہیں۔",
                "biological_treatment": "خوراک: کاپر ہائیڈرو آکسائیڈ اور بائیو ایجنٹ کا اسپرے کریں۔",
                "chemical_treatment": "خوراک: فکسڈ کاپر 2.5 گرام فی لیٹر + مینکوزیب 2 گرام فی لیٹر پانی ملا کر اسپرے کریں۔",
                "prevention": "بیماری سے پاک بیج استعمال کریں اور گرم پانی سے بیج کا علاج کریں۔"
            },
            "ps": {
                "name": "د شملې مرچو باکتریایي ټکي",
                "description": "د مرچو په پاڼو او میوه تاره باکتریایي نښې.",
                "symptoms": "په پاڼو واړه شنه ژېړ داغونه.",
                "biological_treatment": "اندازه: د مسو محلول سپری کړئ.",
                "chemical_treatment": "اندازه: کاپر 2.5 ګرامه + مانکوزیب 2 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "پاک او روغ بیجونه وکاروئ."
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
                "name": "Healthy Plant Leaf",
                "description": "Vibrant foliage with healthy green tissue and no disease symptoms.",
                "symptoms": "Foliage is clear, green, and vigorous.",
                "biological_treatment": "Dosage: Apply balanced organic compost tea or NPK 19-19-19 foliar spray at 3g per Liter water.",
                "chemical_treatment": "No chemical pesticide required.",
                "prevention": "Maintain regular weeding, balanced irrigation, and routine crop scouting."
            },
            "ur": {
                "name": "صحت مند پودا",
                "description": "پودا بالکل صحت مند ہے اور پتوں پر کوئی بیماری نہیں ہے۔",
                "symptoms": "پتا شاداب اور تروتازہ ہے۔",
                "biological_treatment": "خوراک: متوازن نامیاتی کھاد کا استعمال جاری رکھیں۔",
                "chemical_treatment": "کسی کیمیائی اسپرے کی ضرورت نہیں ہے۔",
                "prevention": "معمول کی دیکھ بھال جاری رکھیں۔"
            },
            "ps": {
                "name": "روغ بوټی",
                "description": "بوټی بشپړ روغ دی او هيڅ ناروغي نلري.",
                "symptoms": "پاڼه سمه او شنه ده.",
                "biological_treatment": "عضوي سرې وکاروئ.",
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
        if existing:
            existing.translations = item["translations"]
            existing.crop_name = item["crop_name"]
            existing.scientific_name = item["scientific_name"]
            existing.category = item["category"]
        else:
            disease = Disease(
                disease_key=item["disease_key"],
                crop_name=item["crop_name"],
                scientific_name=item["scientific_name"],
                category=item["category"],
                translations=item["translations"]
            )
            db_session.add(disease)
    db_session.commit()
    print(f"[Seed] Successfully updated/seeded {len(INITIAL_DISEASES)} multi-crop universal diseases with exact dosages.")
