"""
Comprehensive Seed script for Multi-Crop Universal Disease Knowledge Base with Exact Dosages.
Supports English, Urdu, and Pashto for all plant types.
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
        "disease_key": "Citrus_Orange___Haunglongbing_(Citrus_greening)",
        "crop_name": "Citrus",
        "scientific_name": "Candidatus Liberibacter asiaticus",
        "category": "Bacterial",
        "translations": {
            "en": {
                "name": "Citrus Greening (HLB)",
                "description": "Bacterial disease spread by citrus psyllid causing mottled leaves and bitter small fruit.",
                "symptoms": "Asymmetrical yellow mottling on leaves, green misshapen bitter fruit.",
                "biological_treatment": "Dosage: Foliar spray of Micronutrients (Zinc + Manganese + Iron at 2g/L) + Neem Oil (5ml/L).",
                "chemical_treatment": "Dosage: Control psyllid vector using Imidacloprid 17.8% SL (0.5ml per Liter water). PHI: 15 days.",
                "prevention": "Control psyllid insect vector, remove infected trees, use certified clean citrus nursery stock."
            },
            "ur": {
                "name": "سترش اور لیموں کا گریننگ (Citrus Greening)",
                "description": "لیموں اور کینو کے پودوں پر پتوں کا پیلا پڑنا اور پھل کا بدذائقہ ہونا۔",
                "symptoms": "پتوں پر پیلے غیر متوازی دھبے، کینو کے پھل کا چھوٹا اور کڑوا رہ جانا۔",
                "biological_treatment": "خوراک: زنک اور میگنیشیم کی کھاد 2 گرام + نیم کا تیل 5 ملی لیٹر فی لیٹر پانی۔",
                "chemical_treatment": "خوراک: امائڈاکلوپرڈ 0.5 ملی لیٹر فی لیٹر پانی کا اسپرے کریں۔",
                "prevention": "سائلا کیڑے کا خاتمہ کریں اور بیمار پودے تلف کریں۔"
            },
            "ps": {
                "name": "د مالټې او لیمو ګریننګ (Citrus Greening)",
                "description": "د مالټو بوټي ژېړوي او میوه ترخوي.",
                "symptoms": "په پاڼو ژېړې نښې او د میوې خرابېدل.",
                "biological_treatment": "اندازه: مایکرو مغذي مواد 2 ګرامه + نیم تېل 5 ملی لیتر سپری کړئ.",
                "chemical_treatment": "اندازه: امایډاکلوپرډ 0.5 ملي لیتر په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "حشرات مړه کړئ او روغ بوټي وکرئ."
            }
        }
    },
    {
        "disease_key": "Wheat___Leaf_Rust",
        "crop_name": "Wheat",
        "scientific_name": "Puccinia triticina",
        "category": "Fungal",
        "translations": {
            "en": {
                "name": "Wheat Leaf Rust",
                "description": "Fungal rust disease producing orange-red pustules on wheat foliage.",
                "symptoms": "Small reddish-orange pustules scattered on upper leaf surfaces.",
                "biological_treatment": "Dosage: Apply Trichoderma harzianum (5g per Liter water) bio-spray.",
                "chemical_treatment": "Dosage: Spray Tebuconazole 250 EC at 1.0ml per Liter water OR Propiconazole 25% EC at 1.0ml/L. PHI: 30 days.",
                "prevention": "Plant rust-resistant wheat varieties (e.g., Faisalabad-08, Markaz-19)."
            },
            "ur": {
                "name": "گندم کی رتوعی / کنگی (Leaf Rust)",
                "description": "گندم کے پتوں پر نارنجی اور سرخ رنگ کے دانے بنانے والی فنگس۔",
                "symptoms": "پتوں کی اوپری سطح پر چمکدار سرخ اور نارنجی سفوف کے دھبے۔",
                "biological_treatment": "خوراک: ٹرائیکوڈرما 5 گرام فی لیٹر پانی کا اسپرے کریں۔",
                "chemical_treatment": "خوراک: ٹیبوکونازول 1 ملی لیٹر یا پروپیکونازول 1 ملی لیٹر فی لیٹر پانی کا اسپرے کریں۔",
                "prevention": "کنگی سے محفوظ گندم کی قسم کاشت کریں۔"
            },
            "ps": {
                "name": "د غنمو د پاڼو ژېړی (Leaf Rust)",
                "description": "د غنمو په پاڼو نارنجي رنګې ټکې جوړوي.",
                "symptoms": "په پاڼو سرخي او نارنجي سفوف.",
                "biological_treatment": "اندازه: ټرایکوډرما 5 ګرامه په 1 لیتر اوبو کې وکاروئ.",
                "chemical_treatment": "اندازه: ټیبوکونازول 1 ملي لیتر په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "مقاوم غنم وکرئ."
            }
        }
    },
    {
        "disease_key": "Cotton___Bacterial_Blight",
        "crop_name": "Cotton",
        "scientific_name": "Xanthomonas citri pv. malvacearum",
        "category": "Bacterial",
        "translations": {
            "en": {
                "name": "Cotton Bacterial Blight (Angular Leaf Spot)",
                "description": "Bacterial infection causing angular water-soaked leaf spots and boll rot on cotton.",
                "symptoms": "Angular water-soaked spots bounded by leaf veins, black arm lesions on petioles.",
                "biological_treatment": "Dosage: Seed treatment with Pseudomonas fluorescens (10g per kg seed) + Neem cake soil application.",
                "chemical_treatment": "Dosage: Spray Copper Oxychloride (2.5g per Liter water) + Streptomycin Sulphate (0.1g per Liter water).",
                "prevention": "Delint seed with acid, use acid-delinted resistant cotton cultivars."
            },
            "ur": {
                "name": "کپاس کا اینگولر لیف اسپاٹ / بلائٹ",
                "description": "کپاس کے پتوں پر زاویہ دار پانی زدہ داغ پیدا کرنے والا بیکٹیریا۔",
                "symptoms": "پتوں کی رگوں کے درمیان کونے دار سیاہ داغ اور گوبھی کا سڑنا۔",
                "biological_treatment": "خوراک: بیج کا علاج سوڈوموناس 10 گرام فی کلو بیج سے کریں۔",
                "chemical_treatment": "خوراک: کاپر آکسی کلورائڈ 2.5 گرام + اسٹریپٹومائسین 0.1 گرام فی لیٹر پانی۔",
                "prevention": "تیزاب سے علاج شدہ کپاس کا بیج بوئیں۔"
            },
            "ps": {
                "name": "د پنبې او پټیو باکتریایي ناروغي",
                "description": "د پنبې پر پاڼو کونجي داغونه جوړوي.",
                "symptoms": "په پاڼو زاویه‌دار اوبه لرونکي ټکي.",
                "biological_treatment": "اندازه: سوډوموناس 10 ګرامه د یو کیلو تخم لپاره وکاروئ.",
                "chemical_treatment": "اندازه: کاپر 2.5 ګرامه + سټریپټومایسین 0.1 ګرامه سپری کړئ.",
                "prevention": "تصفیه شوی بیج وکرئ."
            }
        }
    },
    {
        "disease_key": "Houseplant___Leaf_Spot",
        "crop_name": "Houseplant",
        "scientific_name": "Cercospora / Phyllosticta spp.",
        "category": "Fungal",
        "translations": {
            "en": {
                "name": "Houseplant & Ornamental Leaf Spot",
                "description": "Fungal leaf spot disease affecting indoor houseplants, potted plants, and ornamentals.",
                "symptoms": "Brown circular leaf spots with yellow margins, premature leaf leaf drop.",
                "biological_treatment": "Dosage: Spray Neem Oil (5ml per Liter water) or Chamomile tea extract every 7 days.",
                "chemical_treatment": "Dosage: Spray Chlorothalonil 75% WP (2.0g per Liter water) or Copper Soap (3ml/L).",
                "prevention": "Avoid wetting foliage indoors, increase room ventilation, wiping leaves clean."
            },
            "ur": {
                "name": "گھریلو پودوں کا لیف اسپاٹ",
                "description": "گھروں کے انڈور اور سجاوٹی پودوں کے پتوں پر بھورے داغ۔",
                "symptoms": "پتوں پر گول بھورے داغ اور پتوں کا وقت سے پہلے گرنا۔",
                "biological_treatment": "خوراک: نیم کا تیل 5 ملی لیٹر فی لیٹر پانی ملا کر 7 دن میں اسپرے کریں۔",
                "chemical_treatment": "خوراک: کلوروتھالونل 2 گرام فی لیٹر پانی ملا کر اسپرے کریں۔",
                "prevention": "انڈور پودوں کے پتوں پر ڈائریکٹ پانی کھڑا نہ ہونے دیں۔"
            },
            "ps": {
                "name": "د کورنیو بوټو پاڼو داغونه",
                "description": "د انډور زېنتي بوټو پر پاڼو نسواري ټکي.",
                "symptoms": "په پاڼو نسواري داغونه او توېدل.",
                "biological_treatment": "اندازه: د نیم تېل 5 ملي لیتر په 1 لیتر اوبو کې سپری کړئ.",
                "chemical_treatment": "اندازه: کلوروتالونیل 2 ګرامه په 1 لیتر اوبو کې سپری کړئ.",
                "prevention": "د بوټو په پاڼو مستقیمې اوبه مه دوئ."
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
