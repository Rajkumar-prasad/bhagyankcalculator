/* Bhagyank Calculator - calculators for all pages (plain JavaScript, no libraries). */
;(function () {
  'use strict'

  const DATA = {"en": {"1": {"number": 1, "planet": "Sun", "planetHindi": "Surya", "title": "The Leader", "keywords": ["Leadership", "Independence", "Ambition"], "summary": "Bhagyank 1 is ruled by the Sun and belongs to natural-born leaders. Your destiny is to pioneer, initiate and stand out. You are independent, confident and driven to create your own path rather than follow others.", "strengths": ["Strong willpower", "Original thinking", "Confidence and authority", "Determination"], "challenges": ["Can be stubborn or egoistic", "Dislikes taking orders", "May become dominating"], "career": "Business ownership, administration, government, leadership roles and entrepreneurship.", "luckyColors": ["Golden", "Yellow", "Orange"], "luckyDays": ["Sunday", "Monday"]}, "2": {"number": 2, "planet": "Moon", "planetHindi": "Chandra", "title": "The Diplomat", "keywords": ["Sensitivity", "Harmony", "Intuition"], "summary": "Bhagyank 2 is ruled by the Moon and reflects emotion, imagination and cooperation. Your destiny is tied to relationships, peace-making and creativity. You are intuitive, gentle and deeply empathetic.", "strengths": ["Great intuition", "Diplomatic and caring", "Creative and artistic", "Team-oriented"], "challenges": ["Over-sensitive", "Indecisive at times", "Mood swings"], "career": "Counselling, arts, hospitality, healthcare, teaching and public relations.", "luckyColors": ["White", "Cream", "Silver"], "luckyDays": ["Monday", "Friday"]}, "3": {"number": 3, "planet": "Jupiter", "planetHindi": "Guru (Brihaspati)", "title": "The Sage", "keywords": ["Wisdom", "Optimism", "Expression"], "summary": "Bhagyank 3 is ruled by Jupiter and blesses you with knowledge, discipline and self-expression. Your destiny is linked to teaching, guidance and growth. You are optimistic, wise and naturally respected.", "strengths": ["Knowledge and wisdom", "Discipline", "Good communication", "Optimistic outlook"], "challenges": ["Can be overly critical", "Tendency to preach", "Impatience"], "career": "Teaching, law, finance, writing, advisory roles and spirituality.", "luckyColors": ["Yellow", "Golden", "Saffron"], "luckyDays": ["Thursday", "Tuesday"]}, "4": {"number": 4, "planet": "Rahu", "planetHindi": "Rahu", "title": "The Rebel", "keywords": ["Discipline", "Uniqueness", "Change"], "summary": "Bhagyank 4 is ruled by Rahu and gives you an unconventional, hardworking and revolutionary destiny. You think differently, question norms and often bring sudden change to the world around you.", "strengths": ["Hardworking", "Practical and systematic", "Unique perspective", "Reliable"], "challenges": ["Rebellious streak", "Feels misunderstood", "Prone to sudden ups and downs"], "career": "Technology, engineering, activism, research and unconventional professions.", "luckyColors": ["Grey", "Blue", "Khaki"], "luckyDays": ["Saturday", "Sunday"]}, "5": {"number": 5, "planet": "Mercury", "planetHindi": "Budh", "title": "The Communicator", "keywords": ["Freedom", "Intelligence", "Versatility"], "summary": "Bhagyank 5 is ruled by Mercury and represents intelligence, adaptability and freedom. Your destiny is dynamic and versatile. You love travel, communication and change, and you learn quickly.", "strengths": ["Sharp intellect", "Excellent communication", "Adaptable", "Business-minded"], "challenges": ["Restlessness", "Overthinking", "Difficulty committing"], "career": "Sales, marketing, media, trading, writing and any communication-driven field.", "luckyColors": ["Green", "Light Blue"], "luckyDays": ["Wednesday", "Friday"]}, "6": {"number": 6, "planet": "Venus", "planetHindi": "Shukra", "title": "The Nurturer", "keywords": ["Love", "Beauty", "Responsibility"], "summary": "Bhagyank 6 is ruled by Venus and is all about love, luxury, beauty and harmony. Your destiny involves caring for others, creating beauty and enjoying the comforts of life. You are charming and family-oriented.", "strengths": ["Loving and caring", "Artistic taste", "Responsible", "Attracts comfort and luxury"], "challenges": ["Over-attachment", "Prone to indulgence", "Worries about loved ones"], "career": "Arts, fashion, design, hospitality, entertainment and beauty industries.", "luckyColors": ["White", "Pink", "Blue"], "luckyDays": ["Friday", "Wednesday"]}, "7": {"number": 7, "planet": "Ketu", "planetHindi": "Ketu", "title": "The Seeker", "keywords": ["Spirituality", "Intuition", "Research"], "summary": "Bhagyank 7 is ruled by Ketu and grants a spiritual, analytical and introspective destiny. You are a deep thinker drawn to mystery, research and the unknown. Your path often leads to wisdom and inner growth.", "strengths": ["Analytical mind", "Spiritual depth", "Independent thinker", "Intuitive"], "challenges": ["Detached or aloof", "Overthinking", "Difficulty trusting"], "career": "Research, spirituality, science, psychology, occult and analytical fields.", "luckyColors": ["Light Grey", "Green", "Cream"], "luckyDays": ["Sunday", "Monday"]}, "8": {"number": 8, "planet": "Saturn", "planetHindi": "Shani", "title": "The Achiever", "keywords": ["Power", "Discipline", "Karma"], "summary": "Bhagyank 8 is ruled by Saturn and represents karma, discipline, justice and material success. Your destiny is built through patience and hard work. Results may come slowly but are lasting and powerful.", "strengths": ["Ambitious", "Disciplined", "Strong sense of justice", "Great endurance"], "challenges": ["Struggle and delays", "Can be rigid", "Emotionally reserved"], "career": "Business, law, real estate, mining, administration and long-term ventures.", "luckyColors": ["Black", "Dark Blue", "Grey"], "luckyDays": ["Saturday", "Friday"]}, "9": {"number": 9, "planet": "Mars", "planetHindi": "Mangal", "title": "The Warrior", "keywords": ["Courage", "Energy", "Compassion"], "summary": "Bhagyank 9 is ruled by Mars and blesses you with courage, energy and a humanitarian heart. Your destiny is one of action, protection and service. You are brave, determined and fight for what is right.", "strengths": ["Courageous", "High energy", "Compassionate", "Determined fighter"], "challenges": ["Quick temper", "Impulsiveness", "Impatience"], "career": "Defence, sports, surgery, engineering, social work and leadership roles.", "luckyColors": ["Red", "Crimson", "Pink"], "luckyDays": ["Tuesday", "Thursday"]}}, "hi": {"1": {"number": 1, "planet": "सूर्य", "title": "नेतृत्वकर्ता", "summary": "भाग्यांक 1 का स्वामी सूर्य है। ऐसे लोग जन्मजात लीडर होते हैं। इनका भाग्य नई शुरुआत करने, आगे बढ़कर नेतृत्व करने और अपनी अलग पहचान बनाने से जुड़ा होता है। ये आत्मनिर्भर, आत्मविश्वासी और महत्वाकांक्षी होते हैं।", "strengths": ["दृढ़ इच्छाशक्ति", "मौलिक सोच", "आत्मविश्वास और अधिकार", "लक्ष्य के प्रति संकल्प"], "challenges": ["ज़िद्दी या अहंकारी हो सकते हैं", "आदेश मानना पसंद नहीं", "हावी होने की प्रवृत्ति"], "career": "अपना व्यवसाय, प्रशासन, सरकारी सेवा, प्रबंधन और उद्यमिता।", "luckyColors": ["सुनहरा", "पीला", "नारंगी"], "luckyDays": ["रविवार", "सोमवार"]}, "2": {"number": 2, "planet": "चंद्र", "title": "कूटनीतिज्ञ", "summary": "भाग्यांक 2 का स्वामी चंद्रमा है। यह भावना, कल्पना और सहयोग का अंक है। इनका भाग्य रिश्तों, शांति स्थापित करने और रचनात्मक कार्यों से जुड़ा होता है। ये संवेदनशील, सहज ज्ञान वाले और दूसरों का दर्द समझने वाले होते हैं।", "strengths": ["तेज़ अंतर्ज्ञान", "कूटनीतिक और देखभाल करने वाले", "रचनात्मक और कलात्मक", "टीम में काम करने वाले"], "challenges": ["ज़रूरत से ज़्यादा भावुक", "कभी-कभी निर्णय लेने में कठिनाई", "मूड में उतार-चढ़ाव"], "career": "काउंसलिंग, कला, होटल व्यवसाय, स्वास्थ्य सेवा, शिक्षण और जनसंपर्क।", "luckyColors": ["सफ़ेद", "क्रीम", "चांदी"], "luckyDays": ["सोमवार", "शुक्रवार"]}, "3": {"number": 3, "planet": "गुरु (बृहस्पति)", "title": "ज्ञानी", "summary": "भाग्यांक 3 का स्वामी गुरु (बृहस्पति) है। यह अंक ज्ञान, अनुशासन और अभिव्यक्ति का आशीर्वाद देता है। इनका भाग्य शिक्षा, मार्गदर्शन और विकास से जुड़ा होता है। ये आशावादी, बुद्धिमान और सम्मानित होते हैं।", "strengths": ["ज्ञान और विवेक", "अनुशासन", "अच्छी वाणी", "सकारात्मक दृष्टिकोण"], "challenges": ["ज़्यादा आलोचना करना", "उपदेश देने की आदत", "अधीरता"], "career": "शिक्षण, कानून, वित्त, लेखन, सलाहकार और आध्यात्मिक क्षेत्र।", "luckyColors": ["पीला", "सुनहरा", "केसरिया"], "luckyDays": ["गुरुवार", "मंगलवार"]}, "4": {"number": 4, "planet": "राहु", "title": "क्रांतिकारी", "summary": "भाग्यांक 4 का स्वामी राहु है। ऐसे लोगों का भाग्य अलग हटकर, मेहनत भरा और बदलाव लाने वाला होता है। ये परंपराओं पर सवाल उठाते हैं, अलग तरह से सोचते हैं और जीवन में अचानक बदलाव देखते हैं।", "strengths": ["कड़ी मेहनत", "व्यावहारिक और व्यवस्थित", "अनोखा दृष्टिकोण", "भरोसेमंद"], "challenges": ["विद्रोही स्वभाव", "लोग इन्हें गलत समझते हैं", "अचानक उतार-चढ़ाव"], "career": "टेक्नोलॉजी, इंजीनियरिंग, रिसर्च, सामाजिक आंदोलन और अलग तरह के पेशे।", "luckyColors": ["स्लेटी", "नीला", "खाकी"], "luckyDays": ["शनिवार", "रविवार"]}, "5": {"number": 5, "planet": "बुध", "title": "संवादकर्ता", "summary": "भाग्यांक 5 का स्वामी बुध है। यह बुद्धि, लचीलेपन और स्वतंत्रता का अंक है। इनका भाग्य गतिशील और बहुमुखी होता है। इन्हें यात्रा, बातचीत और बदलाव पसंद है, और ये बहुत जल्दी सीखते हैं।", "strengths": ["तेज़ बुद्धि", "बेहतरीन संवाद कौशल", "हर स्थिति में ढल जाना", "व्यापारिक समझ"], "challenges": ["बेचैनी", "ज़रूरत से ज़्यादा सोचना", "प्रतिबद्धता में कठिनाई"], "career": "सेल्स, मार्केटिंग, मीडिया, ट्रेडिंग, लेखन और संवाद से जुड़े क्षेत्र।", "luckyColors": ["हरा", "हल्का नीला"], "luckyDays": ["बुधवार", "शुक्रवार"]}, "6": {"number": 6, "planet": "शुक्र", "title": "पालनकर्ता", "summary": "भाग्यांक 6 का स्वामी शुक्र है। यह प्रेम, सुंदरता, सुख-सुविधा और सामंजस्य का अंक है। इनका भाग्य दूसरों की देखभाल करने, सुंदर चीज़ें बनाने और जीवन के सुखों का आनंद लेने से जुड़ा होता है। ये आकर्षक और परिवार-प्रेमी होते हैं।", "strengths": ["प्रेमपूर्ण और देखभाल करने वाले", "कलात्मक रुचि", "ज़िम्मेदार", "सुख-सुविधाओं को आकर्षित करते हैं"], "challenges": ["ज़्यादा लगाव", "भोग-विलास की ओर झुकाव", "प्रियजनों की चिंता"], "career": "कला, फ़ैशन, डिज़ाइन, होटल व्यवसाय, मनोरंजन और ब्यूटी इंडस्ट्री।", "luckyColors": ["सफ़ेद", "गुलाबी", "नीला"], "luckyDays": ["शुक्रवार", "बुधवार"]}, "7": {"number": 7, "planet": "केतु", "title": "साधक", "summary": "भाग्यांक 7 का स्वामी केतु है। यह आध्यात्मिक, विश्लेषणात्मक और आत्मचिंतन वाला भाग्य देता है। ये गहराई से सोचने वाले होते हैं और रहस्य, शोध व अज्ञात चीज़ों की ओर आकर्षित होते हैं। इनका मार्ग ज्ञान और आंतरिक विकास की ओर जाता है।", "strengths": ["विश्लेषण करने वाला दिमाग", "आध्यात्मिक गहराई", "स्वतंत्र विचारक", "अंतर्ज्ञानी"], "challenges": ["दूसरों से दूरी बनाना", "ज़्यादा सोचना", "भरोसा करने में कठिनाई"], "career": "रिसर्च, अध्यात्म, विज्ञान, मनोविज्ञान, गूढ़ विद्या और विश्लेषण से जुड़े क्षेत्र।", "luckyColors": ["हल्का स्लेटी", "हरा", "क्रीम"], "luckyDays": ["रविवार", "सोमवार"]}, "8": {"number": 8, "planet": "शनि", "title": "उपलब्धि पाने वाला", "summary": "भाग्यांक 8 का स्वामी शनि है। यह कर्म, अनुशासन, न्याय और भौतिक सफलता का अंक है। इनका भाग्य धैर्य और कड़ी मेहनत से बनता है। सफलता देर से मिल सकती है, लेकिन जो मिलती है वह स्थायी और मज़बूत होती है।", "strengths": ["महत्वाकांक्षी", "अनुशासित", "न्यायप्रिय", "बहुत सहनशील"], "challenges": ["संघर्ष और देरी", "कठोर हो सकते हैं", "भावनाएँ ज़ाहिर नहीं करते"], "career": "व्यवसाय, कानून, रियल एस्टेट, खनन, प्रशासन और लंबे समय के प्रोजेक्ट।", "luckyColors": ["काला", "गहरा नीला", "स्लेटी"], "luckyDays": ["शनिवार", "शुक्रवार"]}, "9": {"number": 9, "planet": "मंगल", "title": "योद्धा", "summary": "भाग्यांक 9 का स्वामी मंगल है। यह साहस, ऊर्जा और मानवता की सेवा का अंक है। इनका भाग्य कर्म, रक्षा और सेवा से जुड़ा होता है। ये बहादुर, दृढ़ निश्चयी होते हैं और सही बात के लिए लड़ते हैं।", "strengths": ["साहसी", "भरपूर ऊर्जा", "दयालु", "हार न मानने वाले"], "challenges": ["जल्दी गुस्सा", "जल्दबाज़ी", "अधीरता"], "career": "सेना और रक्षा, खेल, सर्जरी, इंजीनियरिंग, समाज सेवा और नेतृत्व।", "luckyColors": ["लाल", "गहरा लाल", "गुलाबी"], "luckyDays": ["मंगलवार", "गुरुवार"]}}, "mr": {"1": {"number": 1, "planet": "सूर्य", "title": "नेतृत्व करणारा", "summary": "भाग्यांक 1 चा स्वामी सूर्य आहे. अशी माणसे जन्मजात नेते असतात. नवी सुरुवात करणे, पुढे होऊन जबाबदारी घेणे आणि स्वतःची वेगळी ओळख तयार करणे हेच यांचे भाग्य असते. ही माणसे आत्मविश्वासू, स्वतंत्र आणि महत्त्वाकांक्षी असतात.", "strengths": ["दृढ इच्छाशक्ती", "स्वतःचे नवे विचार", "आत्मविश्वास आणि अधिकार", "ध्येयासाठी जिद्द"], "challenges": ["हट्टी किंवा अहंकारी होऊ शकतात", "आदेश ऐकायला आवडत नाही", "इतरांवर वर्चस्व गाजवण्याची सवय"], "career": "स्वतःचा व्यवसाय, प्रशासन, सरकारी नोकरी, व्यवस्थापन आणि उद्योजकता.", "luckyColors": ["सोनेरी", "पिवळा", "नारिंगी"], "luckyDays": ["रविवार", "सोमवार"]}, "2": {"number": 2, "planet": "चंद्र", "title": "समजूतदार मध्यस्थ", "summary": "भाग्यांक 2 चा स्वामी चंद्र आहे. हा भावना, कल्पना आणि सहकार्याचा अंक आहे. नाती जपणे, वाद मिटवणे आणि सर्जनशील काम करणे यांच्याशी यांचे भाग्य जोडलेले असते. ही माणसे हळवी, अंतर्ज्ञानी आणि इतरांचे दुःख समजून घेणारी असतात.", "strengths": ["उत्तम अंतर्ज्ञान", "समजूतदार आणि काळजी घेणारे", "कलात्मक आणि सर्जनशील", "टीममध्ये छान काम करणारे"], "challenges": ["गरजेपेक्षा जास्त हळवे", "कधी कधी निर्णय घेणे अवघड", "मूड लवकर बदलतो"], "career": "समुपदेशन, कला, हॉटेल व्यवसाय, आरोग्यसेवा, शिक्षण आणि जनसंपर्क.", "luckyColors": ["पांढरा", "क्रीम", "चंदेरी"], "luckyDays": ["सोमवार", "शुक्रवार"]}, "3": {"number": 3, "planet": "गुरू (बृहस्पती)", "title": "ज्ञानी", "summary": "भाग्यांक 3 चा स्वामी गुरू आहे. हा अंक ज्ञान, शिस्त आणि स्वतःला व्यक्त करण्याची ताकद देतो. शिक्षण, मार्गदर्शन आणि प्रगती यांच्याशी यांचे भाग्य जोडलेले असते. ही माणसे आशावादी, हुशार आणि आदरणीय असतात.", "strengths": ["ज्ञान आणि विवेक", "शिस्त", "उत्तम बोलणे", "सकारात्मक दृष्टिकोन"], "challenges": ["जास्त टीका करण्याची सवय", "उपदेश देण्याची सवय", "अधीरपणा"], "career": "शिक्षण, कायदा, वित्त, लेखन, सल्लागार आणि अध्यात्म.", "luckyColors": ["पिवळा", "सोनेरी", "भगवा"], "luckyDays": ["गुरुवार", "मंगळवार"]}, "4": {"number": 4, "planet": "राहू", "title": "वेगळ्या वाटेने जाणारा", "summary": "भाग्यांक 4 चा स्वामी राहू आहे. अशा माणसांचे भाग्य वेगळे, मेहनतीचे आणि बदल घडवणारे असते. ही माणसे परंपरांवर प्रश्न विचारतात, वेगळा विचार करतात आणि आयुष्यात अचानक बदल अनुभवतात.", "strengths": ["कष्टाळू", "व्यावहारिक आणि नीटनेटके", "वेगळा दृष्टिकोन", "विश्वासू"], "challenges": ["बंडखोर स्वभाव", "लोक यांना चुकीचे समजतात", "अचानक चढ-उतार"], "career": "तंत्रज्ञान, इंजिनिअरिंग, संशोधन, सामाजिक चळवळ आणि वेगळ्या प्रकारचे व्यवसाय.", "luckyColors": ["राखाडी", "निळा", "खाकी"], "luckyDays": ["शनिवार", "रविवार"]}, "5": {"number": 5, "planet": "बुध", "title": "संवाद साधणारा", "summary": "भाग्यांक 5 चा स्वामी बुध आहे. हा बुद्धी, लवचिकता आणि स्वातंत्र्याचा अंक आहे. यांचे भाग्य गतिमान आणि बहुरंगी असते. यांना प्रवास, गप्पा आणि बदल आवडतात आणि ही माणसे पटकन शिकतात.", "strengths": ["तल्लख बुद्धी", "उत्तम संवाद कौशल्य", "कोणत्याही परिस्थितीत जुळवून घेणारे", "व्यापाराची समज"], "challenges": ["अस्वस्थपणा", "गरजेपेक्षा जास्त विचार", "एका गोष्टीला चिकटून राहणे अवघड"], "career": "विक्री, मार्केटिंग, मीडिया, ट्रेडिंग, लेखन आणि संवादाशी संबंधित क्षेत्रे.", "luckyColors": ["हिरवा", "फिकट निळा"], "luckyDays": ["बुधवार", "शुक्रवार"]}, "6": {"number": 6, "planet": "शुक्र", "title": "सांभाळ करणारा", "summary": "भाग्यांक 6 चा स्वामी शुक्र आहे. हा प्रेम, सौंदर्य, सुखसोयी आणि सुसंवादाचा अंक आहे. इतरांची काळजी घेणे, सुंदर गोष्टी घडवणे आणि आयुष्याचा आनंद घेणे यांच्याशी यांचे भाग्य जोडलेले असते. ही माणसे आकर्षक आणि कुटुंबप्रेमी असतात.", "strengths": ["प्रेमळ आणि काळजी घेणारे", "कलात्मक आवड", "जबाबदार", "सुखसोयी आकर्षित करतात"], "challenges": ["जास्त ओढ लावून घेणे", "चैनीकडे कल", "प्रियजनांची काळजी करत राहणे"], "career": "कला, फॅशन, डिझाइन, हॉटेल व्यवसाय, मनोरंजन आणि सौंदर्य क्षेत्र.", "luckyColors": ["पांढरा", "गुलाबी", "निळा"], "luckyDays": ["शुक्रवार", "बुधवार"]}, "7": {"number": 7, "planet": "केतू", "title": "साधक", "summary": "भाग्यांक 7 चा स्वामी केतू आहे. हा अंक आध्यात्मिक, विचारशील आणि आत्मचिंतन करणारे भाग्य देतो. ही माणसे खोलवर विचार करतात आणि गूढ गोष्टी, संशोधन आणि अज्ञात विषयांकडे ओढली जातात. यांचा मार्ग ज्ञान आणि आतल्या प्रगतीकडे जातो.", "strengths": ["विश्लेषण करणारे मन", "आध्यात्मिक खोली", "स्वतंत्र विचार", "अंतर्ज्ञान"], "challenges": ["इतरांपासून अंतर ठेवणे", "जास्त विचार करणे", "विश्वास ठेवायला वेळ लागतो"], "career": "संशोधन, अध्यात्म, विज्ञान, मानसशास्त्र, गूढविद्या आणि विश्लेषणाची कामे.", "luckyColors": ["फिकट राखाडी", "हिरवा", "क्रीम"], "luckyDays": ["रविवार", "सोमवार"]}, "8": {"number": 8, "planet": "शनी", "title": "यश मिळवणारा", "summary": "भाग्यांक 8 चा स्वामी शनी आहे. हा कर्म, शिस्त, न्याय आणि भौतिक यशाचा अंक आहे. यांचे भाग्य संयम आणि कष्टातून घडते. यश उशिरा मिळू शकते, पण जे मिळते ते टिकाऊ आणि भक्कम असते.", "strengths": ["महत्त्वाकांक्षी", "शिस्तप्रिय", "न्यायप्रिय", "खूप सहनशील"], "challenges": ["संघर्ष आणि उशीर", "कठोर होऊ शकतात", "भावना पटकन व्यक्त करत नाहीत"], "career": "व्यवसाय, कायदा, रिअल इस्टेट, खाणकाम, प्रशासन आणि दीर्घकालीन प्रकल्प.", "luckyColors": ["काळा", "गडद निळा", "राखाडी"], "luckyDays": ["शनिवार", "शुक्रवार"]}, "9": {"number": 9, "planet": "मंगळ", "title": "योद्धा", "summary": "भाग्यांक 9 चा स्वामी मंगळ आहे. हा धैर्य, ऊर्जा आणि माणुसकीच्या सेवेचा अंक आहे. कृती, रक्षण आणि सेवा यांच्याशी यांचे भाग्य जोडलेले असते. ही माणसे धाडसी, जिद्दी असतात आणि योग्य गोष्टीसाठी लढतात.", "strengths": ["धाडसी", "भरपूर ऊर्जा", "दयाळू", "हार न मानणारे"], "challenges": ["पटकन राग येतो", "घाई करणे", "अधीरपणा"], "career": "सैन्य आणि संरक्षण, खेळ, शस्त्रक्रिया, इंजिनिअरिंग, समाजसेवा आणि नेतृत्व.", "luckyColors": ["लाल", "गडद लाल", "गुलाबी"], "luckyDays": ["मंगळवार", "गुरुवार"]}}};

  var MONTHS = {
    en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    hi: ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'],
    mr: ['जानेवारी', 'फेब्रुवारी', 'मार्च', 'एप्रिल', 'मे', 'जून', 'जुलै', 'ऑगस्ट', 'सप्टेंबर', 'ऑक्टोबर', 'नोव्हेंबर', 'डिसेंबर'],
  }

  var TEXT = {
    en: {
      missing: 'Please select your full date of birth.',
      invalid: 'This date does not exist. Please check the day and month.',
      badge: 'Bhagyank',
      yourNumber: 'Your Destiny Number is',
      planet: 'Ruling Planet',
      mulank: 'Mulank',
      strengths: 'Strengths',
      challenges: 'Watch-Outs',
      careers: 'Ideal Careers',
      lucky: 'Lucky Colors &amp; Days',
      calc: function (t, b) {
        return 'Calculation: all digits of your date of birth add up to ' + t + ', which reduces to Bhagyank ' + b + '.'
      },
      more: function (b) { return 'Full Bhagyank ' + b + ' meaning' },
      loshu: 'Make my Lo Shu Grid',
      shareBtn: 'Share on WhatsApp',
      share: function (b, title) {
        return 'My Bhagyank is ' + b + ' (' + title + '). Find yours free: https://www.bhagyank-calculator.online/'
      },
    },
    hi: {
      missing: 'कृपया अपनी पूरी जन्मतिथि चुनें।',
      invalid: 'यह तारीख़ मौजूद नहीं है। कृपया दिन और महीना जाँचें।',
      badge: 'भाग्यांक',
      yourNumber: 'आपका भाग्यांक है',
      planet: 'स्वामी ग्रह',
      mulank: 'मूलांक',
      strengths: 'खूबियाँ',
      challenges: 'सावधानियाँ',
      careers: 'उपयुक्त करियर',
      lucky: 'शुभ रंग और दिन',
      calc: function (t, b) {
        return 'गणना: आपकी जन्मतिथि के सभी अंकों का योग ' + t + ' है, जिसे एक अंक में बदलने पर भाग्यांक ' + b + ' आता है।'
      },
      more: function (b) { return 'भाग्यांक ' + b + ' का पूरा अर्थ' },
      loshu: 'लो शू ग्रिड बनाएँ',
      shareBtn: 'WhatsApp पर शेयर करें',
      share: function (b, title) {
        return 'मेरा भाग्यांक ' + b + ' (' + title + ') है। अपना भाग्यांक मुफ़्त में जानें: https://www.bhagyank-calculator.online/hi'
      },
    },
    mr: {
      missing: 'कृपया तुमची पूर्ण जन्मतारीख निवडा.',
      invalid: 'ही तारीख अस्तित्वात नाही. कृपया दिवस आणि महिना तपासा.',
      badge: 'भाग्यांक',
      yourNumber: 'तुमचा भाग्यांक आहे',
      planet: 'स्वामी ग्रह',
      mulank: 'मूलांक',
      strengths: 'गुणवैशिष्ट्ये',
      challenges: 'लक्ष द्या',
      careers: 'योग्य करिअर',
      lucky: 'शुभ रंग आणि दिवस',
      calc: function (t, b) {
        return 'गणना: तुमच्या जन्मतारखेच्या सर्व अंकांची बेरीज ' + t + ' आहे, जिचा एक अंक केल्यावर भाग्यांक ' + b + ' येतो.'
      },
      more: function (b) { return 'भाग्यांक ' + b + ' चा संपूर्ण अर्थ' },
      loshu: 'लो शू ग्रिड बनवा',
      shareBtn: 'WhatsApp वर शेअर करा',
      share: function (b, title) {
        return 'माझा भाग्यांक ' + b + ' (' + title + ') आहे. तुमचा भाग्यांक मोफत जाणून घ्या: https://www.bhagyank-calculator.online/mr'
      },
    },
  }

  var ICON =
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l1.9 5.6L19.5 9.5l-5.6 1.9L12 17l-1.9-5.6L4.5 9.5l5.6-1.9L12 2z" fill="currentColor"/></svg>'

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    })
  }

  function reduce(n) {
    n = Math.abs(n)
    while (n > 9) {
      n = String(n).split('').reduce(function (s, d) { return s + Number(d) }, 0)
    }
    return n
  }

  function digitSum(str) {
    return String(str).split('').reduce(function (s, d) { return s + (Number(d) || 0) }, 0)
  }

  function daysInMonth(month, year) {
    // Before a year is chosen, allow 29 Feb (leap year).
    return new Date(year || 2000, month, 0).getDate()
  }

  function scrollTo(el) {
    if (!el) return
    requestAnimationFrame(function () {
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    })
  }

  function fill(select, values, labels) {
    var keep = select.value
    var first = select.options[0]
    select.innerHTML = ''
    select.appendChild(first)
    values.forEach(function (v, i) {
      var o = document.createElement('option')
      o.value = v
      o.textContent = labels ? labels[i] : v
      select.appendChild(o)
    })
    if (keep && values.map(String).indexOf(keep) !== -1) select.value = keep
  }

  function range(a, b) {
    var out = []
    for (var i = a; i <= b; i++) out.push(i)
    return out
  }

  /* Day / month / year selects that only offer real dates. */
  function setupDob(root, lang) {
    var day = root.querySelector('[data-dob="day"]')
    var month = root.querySelector('[data-dob="month"]')
    var year = root.querySelector('[data-dob="year"]')
    fill(month, range(1, 12), MONTHS[lang])
    if (year) {
      var now = new Date().getFullYear()
      fill(year, range(now - 119, now).reverse())
    }
    function updateDays() {
      var max = month.value ? daysInMonth(Number(month.value), year ? Number(year.value) : 0) : 31
      fill(day, range(1, max))
    }
    updateDays()
    month.addEventListener('change', updateDays)
    if (year) year.addEventListener('change', updateDays)
    return { day: day, month: month, year: year }
  }

  function showError(form, msg) {
    var p = form.querySelector('.error')
    p.textContent = msg || ''
    p.hidden = !msg
  }

  function list(items) {
    return '<ul>' + items.map(function (s) { return '<li>' + esc(s) + '</li>' }).join('') + '</ul>'
  }

  /* ---------------- Bhagyank ---------------- */
  function bhagyank(root) {
    var lang = TEXT[root.getAttribute('data-lang')] ? root.getAttribute('data-lang') : 'en'
    var t = TEXT[lang]
    var form = root.querySelector('form')
    var out = root.querySelector('.result')
    var f = setupDob(root, lang)

    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!f.day.value || !f.month.value || !f.year.value) return showError(form, t.missing)
      var d = Number(f.day.value), m = Number(f.month.value), y = Number(f.year.value)
      if (d > daysInMonth(m, y)) return showError(form, t.invalid)
      showError(form, '')

      var total = digitSum('' + d + m + y)
      var b = reduce(total)
      var mul = reduce(d)
      var en = DATA.en[b]
      var info = lang === 'en' ? en : DATA[lang][b]
      var planet = lang === 'en' ? en.planet + ' (' + en.planetHindi + ')' : info.planet

      out.innerHTML =
        '<div class="card result-card">' +
        '<div class="result-top"><div class="circle"><span>' + b + '</span><small>' + t.badge + '</small></div>' +
        '<div><p class="muted small">' + t.yourNumber + '</p><h3 class="result-title">' + b + ' - ' + esc(info.title) + '</h3>' +
        '<div class="chips"><span class="chip">' + t.planet + ': ' + esc(planet) + '</span>' +
        '<span class="chip">' + t.mulank + ': ' + mul + '</span></div></div></div>' +
        '<p class="result-summary">' + esc(info.summary) + '</p>' +
        '<div class="info-grid">' +
        '<div class="info"><h4>' + ICON + ' ' + t.strengths + '</h4>' + list(info.strengths) + '</div>' +
        '<div class="info"><h4 class="accent">' + ICON + ' ' + t.challenges + '</h4>' + list(info.challenges) + '</div>' +
        '<div class="info"><h4>' + ICON + ' ' + t.careers + '</h4><p>' + esc(info.career) + '</p></div>' +
        '<div class="info"><h4>' + ICON + ' ' + t.lucky + '</h4><p>' + esc(info.luckyColors.join(', ')) + '<br>' +
        esc(info.luckyDays.join(', ')) + '</p></div>' +
        '</div><p class="xs muted calc-note">' + t.calc(total, b) + '</p>' +
        '<div class="result-actions">' +
        '<a class="btn inline" href="' + (lang === 'en' ? '/bhagyank/' : '/' + lang + '/bhagyank/') + b + '">' + t.more(b) + '</a>' +
        '<a class="btn inline ghost" href="/lo-shu-grid-calculator">' + t.loshu + '</a>' +
        '<a class="btn inline ghost" target="_blank" rel="noopener" href="https://wa.me/?text=' +
        encodeURIComponent(t.share(b, info.title)) + '">' + t.shareBtn + '</a>' +
        '</div></div>'
      scrollTo(out)
    })
  }

  /* ---------------- Lo Shu grid ---------------- */
  var LS_ORDER = [4, 9, 2, 3, 5, 7, 8, 1, 6]
  var LS_PLANES = [
    ['Mental plane', [4, 9, 2]], ['Emotional plane', [3, 5, 7]], ['Practical plane', [8, 1, 6]],
    ['Thought plane', [4, 3, 8]], ['Will plane', [9, 5, 1]], ['Action plane', [2, 7, 6]],
    ['Golden Yog', [4, 5, 6]], ['Silver Yog', [2, 5, 8]],
  ]
  var LS_AREA = {
    1: 'communication and career', 2: 'feelings and intuition', 3: 'learning and imagination',
    4: 'order and hard work', 5: 'balance and focus', 6: 'family, home and comforts',
    7: 'inner growth and luck', 8: 'money handling and patience', 9: 'energy and ambition',
  }

  function loshu(root) {
    var form = root.querySelector('form')
    var out = root.querySelector('.result')
    var f = setupDob(root, 'en')
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!f.day.value || !f.month.value || !f.year.value) return showError(form, 'Please select your full date of birth.')
      var d = Number(f.day.value), m = Number(f.month.value), y = Number(f.year.value)
      if (d > daysInMonth(m, y)) return showError(form, 'This date does not exist. Please check the day and month.')
      showError(form, '')
      var digits = ('' + d + m + y).split('').map(Number).filter(function (x) { return x > 0 })
      var mul = reduce(d)
      var bhag = reduce(digitSum('' + d + m + y))
      var all = digits.concat([mul, bhag])
      var count = {}
      all.forEach(function (x) { count[x] = (count[x] || 0) + 1 })
      var cells = LS_ORDER.map(function (k) {
        var v = count[k] ? new Array(count[k] + 1).join(String(k)) : ''
        return '<div class="ls-cell' + (v ? '' : ' ls-empty') + '"><span class="ls-pos">' + k + '</span><span class="ls-val">' + v + '</span></div>'
      }).join('')
      var missing = [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(function (k) { return !count[k] })
      var repeated = [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(function (k) { return count[k] > 1 })
      var planes = LS_PLANES.filter(function (p) { return p[1].every(function (k) { return count[k] }) })
      out.innerHTML =
        '<div class="card result-card">' +
        '<div class="ls-result"><div class="ls-grid" aria-label="Your Lo Shu Grid">' + cells + '</div>' +
        '<div><p class="muted small">Your Lo Shu Grid</p><h3 class="result-title">' + d + '-' + m + '-' + y + '</h3>' +
        '<div class="chips"><span class="chip">Mulank: ' + mul + '</span><span class="chip">Bhagyank: ' + bhag + '</span></div>' +
        '<p class="xs muted calc-note">Digits used: ' + digits.join(', ') + ' + Mulank ' + mul + ' + Bhagyank ' + bhag + ' (zeros are left out)</p></div></div>' +
        '<div class="info-grid">' +
        '<div class="info"><h4>Complete planes</h4>' + (planes.length ? list(planes.map(function (p) { return p[0] + ' (' + p[1].join('-') + ')' })) : '<p>No complete plane - that is very common.</p>') + '</div>' +
        '<div class="info"><h4>Repeated numbers</h4>' + (repeated.length ? list(repeated.map(function (k) { return k + ' x' + count[k] + ' - strong ' + LS_AREA[k] })) : '<p>None</p>') + '</div>' +
        '<div class="info" style="grid-column:1/-1"><h4 class="accent">Missing numbers</h4>' + (missing.length ? list(missing.map(function (k) { return k + ' - may need effort in ' + LS_AREA[k] })) : '<p>None - every number is present.</p>') + '</div>' +
        '</div>' +
        '<div class="result-actions"><a class="btn inline" href="/bhagyank/' + bhag + '">Read Bhagyank ' + bhag + ' meaning</a></div>' +
        '</div>'
      scrollTo(out)
    })
  }

  /* ---------------- Moolank ---------------- */
  function moolank(root) {
    var form = root.querySelector('form')
    var out = root.querySelector('.result')
    var f = setupDob(root, 'en')
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!f.day.value || !f.month.value) return showError(form, 'Please select your birth day and month.')
      var d = Number(f.day.value)
      if (d > daysInMonth(Number(f.month.value), 0)) return showError(form, 'This date does not exist. Please check the day and month.')
      showError(form, '')
      var m = reduce(d)
      var info = DATA.en[m]
      out.innerHTML =
        '<div class="card result-card">' +
        '<div class="result-top"><div class="circle"><span>' + m + '</span><small>Moolank</small></div>' +
        '<div><p class="muted small">Your Birth Number is</p><h3 class="result-title">' + m + ' - ' + esc(info.title) + '</h3>' +
        '<div class="chips"><span class="chip">Ruling Planet: ' + esc(info.planet + ' (' + info.planetHindi + ')') + '</span></div></div></div>' +
        '<p class="result-summary">' + esc(info.summary) + '</p>' +
        '<div class="info-grid">' +
        '<div class="info"><h4>Personality strengths</h4>' + list(info.strengths) + '</div>' +
        '<div class="info"><h4 class="accent">Suitable careers</h4><p>' + esc(info.career) + '</p></div>' +
        '</div><p class="xs muted calc-note">Your Moolank is calculated by reducing your birth day, ' + d + ', to a single digit.</p></div>'
      scrollTo(out)
    })
  }

  /* ---------------- Namank ---------------- */
  var LETTERS = {
    a: 1, i: 1, j: 1, q: 1, y: 1, b: 2, k: 2, r: 2, c: 3, g: 3, l: 3, s: 3, d: 4, m: 4, t: 4,
    e: 5, h: 5, n: 5, x: 5, u: 6, v: 6, w: 6, o: 7, z: 7, f: 8, p: 8,
  }
  var NAMANK = {
    1: ['The Leader', 'Independent, ambitious and confident energy.'],
    2: ['The Diplomat', 'Cooperative, intuitive and emotionally aware energy.'],
    3: ['The Creator', 'Expressive, optimistic and socially magnetic energy.'],
    4: ['The Builder', 'Practical, disciplined and dependable energy.'],
    5: ['The Explorer', 'Adaptable, curious and freedom-loving energy.'],
    6: ['The Nurturer', 'Caring, artistic and harmony-seeking energy.'],
    7: ['The Seeker', 'Thoughtful, spiritual and analytical energy.'],
    8: ['The Achiever', 'Organised, determined and results-focused energy.'],
    9: ['The Humanitarian', 'Compassionate, courageous and generous energy.'],
  }

  function namank(root) {
    var form = root.querySelector('form')
    var input = form.querySelector('input')
    var btn = form.querySelector('button')
    var out = root.querySelector('.tool-result')
    input.addEventListener('input', function () {
      var clean = input.value.replace(/[^a-zA-Z ]/g, '')
      if (clean !== input.value) input.value = clean
      btn.disabled = !clean.trim()
    })
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      var name = input.value.trim()
      var total = name.toLowerCase().split('').reduce(function (s, c) { return s + (LETTERS[c] || 0) }, 0)
      if (!total) return
      var n = reduce(total)
      out.innerHTML =
        '<div class="tool-out"><p class="eyebrow">Your Namank</p><p class="big-num">' + n + '</p>' +
        '<p class="result-title">' + NAMANK[n][0] + '</p><p class="muted">' + NAMANK[n][1] + '</p>' +
        '<p class="small muted">Name analysed: ' + esc(name) + '</p>' +
        '<button type="button" class="text-btn" data-reset>Try another name</button></div>'
      out.querySelector('[data-reset]').addEventListener('click', function () {
        input.value = ''
        btn.disabled = true
        out.innerHTML = ''
        input.focus()
      })
      scrollTo(out)
    })
  }

  /* ---------------- Gemstone ---------------- */
  var STONES = {
    1: ['Ruby', 'माणिक्य', 'Sun', 'Confidence, leadership and vitality', 'Red'],
    2: ['Pearl', 'मोती', 'Moon', 'Emotional balance and calmness', 'White'],
    3: ['Yellow Sapphire', 'पुखराज', 'Jupiter', 'Wisdom, growth and prosperity', 'Yellow'],
    4: ['Hessonite', 'गोमेद', 'Rahu', 'Focus, courage and stability', 'Honey brown'],
    5: ['Emerald', 'पन्ना', 'Mercury', 'Communication, learning and creativity', 'Green'],
    6: ['Diamond', 'हीरा', 'Venus', 'Love, beauty and harmony', 'White'],
    7: ["Cat's Eye", 'लहसुनिया', 'Ketu', 'Intuition, protection and spirituality', 'Greenish gold'],
    8: ['Blue Sapphire', 'नीलम', 'Saturn', 'Discipline, patience and progress', 'Blue'],
    9: ['Red Coral', 'मूंगा', 'Mars', 'Energy, courage and determination', 'Red-orange'],
  }

  function gemstone(root) {
    var form = root.querySelector('form')
    var input = form.querySelector('input')
    var btn = form.querySelector('button')
    var out = root.querySelector('.tool-result')
    input.max = new Date().toISOString().split('T')[0]
    input.addEventListener('input', function () { btn.disabled = !input.value })
    input.addEventListener('change', function () { btn.disabled = !input.value })
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!input.value) return
      var n = reduce(Number(input.value.split('-')[2]))
      var s = STONES[n]
      out.innerHTML =
        '<div class="tool-out"><p class="eyebrow">Your recommended gemstone</p>' +
        '<p class="result-title big">' + esc(s[0]) + '</p><p class="muted">' + s[1] + ' · Gemstone for Number ' + n + '</p>' +
        '<div class="stats"><div><p class="xs muted">Ruling planet</p><p>' + s[2] + '</p></div>' +
        '<div><p class="xs muted">Traditional benefit</p><p>' + s[3] + '</p></div>' +
        '<div><p class="xs muted">Associated color</p><p>' + s[4] + '</p></div></div>' +
        '<button type="button" class="text-btn" data-reset>Try another date</button></div>'
      out.querySelector('[data-reset]').addEventListener('click', function () {
        input.value = ''
        btn.disabled = true
        out.innerHTML = ''
      })
      scrollTo(out)
    })
  }

  var INIT = { bhagyank: bhagyank, moolank: moolank, namank: namank, gemstone: gemstone, loshu: loshu }

  document.querySelectorAll('[data-calc]').forEach(function (el) {
    var fn = INIT[el.getAttribute('data-calc')]
    if (fn) fn(el)
  })

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear()
  })
})()
