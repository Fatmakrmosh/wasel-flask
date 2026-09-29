from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# قاعدة بيانات منصة واصل
DB = {
    "announcement": "✨ مرحباً بكم في واصل اليوم: حجز رحلات الليموزين، البكاسي، الشرائح، الباصات، والدفارات لنقل البضائع والطرود لكل المدن.",
    "bankak_account": "9824691",
    "bankak_name": "شركة واصل لخدمات النقل والليموزين",
    
    # حسابات الإدارة والمشرفين
    "admin_users": {
        "admin": {
            "username": "admin",
            "name": "المدير العام (إدارة منصة واصل)",
            "phone": "0912300000",
            "national_id": "10123456789",
            "photo": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150",
            "pass": "admin123",
            "pledge_agreed": True,
            "role_title": "المدير العام (صلاحيات كاملة)"
        },
        "sup1": {
            "username": "sup1",
            "name": "عمر خالد - مشرف حركة الرحلات والمواقف",
            "phone": "0912300001",
            "national_id": "10123456780",
            "photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150",
            "pass": "sup123",
            "pledge_agreed": True,
            "role_title": "مشرف حركة الرحلات"
        },
        "sup2": {
            "username": "sup2",
            "name": "ياسر عثمان - مشرف الشركات والدفارات والسائقين",
            "phone": "0912300002",
            "national_id": "10123456781",
            "photo": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150",
            "pass": "sup223",
            "pledge_agreed": True,
            "role_title": "مشرف الشركات والشحن"
        }
    },
    "companies": [
        {"id": 1, "name": "شركة النيل السريع للنقل الشامل", "contact": "0912345678", "website": "https://nile-express.sd"},
        {"id": 2, "name": "شركة البركة والرضا لليموزين والشحن", "contact": "0987654321", "website": "https://facebook.com/albaraka.transport"}
    ],
    "drivers": [
        {
            "id": 1,
            "name": "أحمد عبد الله مصطفى",
            "national_id": "10293847561",
            "phone": "0912300001",
            "vehicle_model": "تويوتا ليموزين كامري فاخرة",
            "vehicle_color": "أبيض لؤلؤي",
            "vehicle_year": "2024",
            "plate_no": "خ5-4321",
            "license_expiry": "2028-12-30",
            "photo": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150",
            "license_photo": "مستند رخصة قيادة عامة معتمد",
            "reg_photo": "ترخيص سير مركبة ساري"
        },
        {
            "id": 2,
            "name": "عثمان العوض محمد",
            "national_id": "10987654321",
            "phone": "0922200002",
            "vehicle_model": "دفار جامبو (سعة نقل بضائع)",
            "vehicle_color": "أزرق ملكي",
            "vehicle_year": "2023",
            "plate_no": "خ2-8811",
            "license_expiry": "2027-09-20",
            "photo": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150",
            "license_photo": "مستند رخصة قيادة نقل معتمد",
            "reg_photo": "ترخيص سير شاحنة بضائع"
        }
    ],
    "routes": [
        {"id": "route_1", "name": "بحري - شندي والعكس", "from": "بحري", "to": "شندي"},
        {"id": "route_2", "name": "بحري - عطبرة والعكس", "from": "بحري", "to": "عطبرة"},
        {"id": "route_3", "name": "بحري - مروي - كريمة والعكس", "from": "بحري", "to": "مروي - كريمة"}
    ],
    "trips": [
        # بحري - شندي والعكس
        {"id": 101, "route_id": "route_1", "from": "بحري", "to": "شندي", "vehicle_type": "ليموزين فاخرة (4 ركاب)", "time": "06:30 صباحاً", "seat_price": 30000, "full_price": 120000, "capacity": 4, "booked": 1, "station": "موقف شندي - بحري", "tickets": ["WSL-1011"], "type_key": "limo"},
        {"id": 102, "route_id": "route_1", "from": "بحري", "to": "شندي", "vehicle_type": "بكسي دبل كاب خاص (4 ركاب)", "time": "07:30 صباحاً", "seat_price": 28000, "full_price": 110000, "capacity": 4, "booked": 0, "station": "موقف شندي - بحري", "tickets": [], "type_key": "pickup"},
        {"id": 103, "route_id": "route_1", "from": "بحري", "to": "شندي", "vehicle_type": "شريحة تويوتا (17 راكب)", "time": "08:30 صباحاً", "seat_price": 18000, "full_price": 280000, "capacity": 17, "booked": 5, "station": "موقف شندي - بحري", "tickets": ["WSL-1012"], "type_key": "van"},
        {"id": 104, "route_id": "route_1", "from": "بحري", "to": "شندي", "vehicle_type": "باص سفري فاخر (45 راكب)", "time": "09:30 صباحاً", "seat_price": 12000, "full_price": 500000, "capacity": 45, "booked": 18, "station": "الميناء البري - بحري", "tickets": ["WSL-1013"], "type_key": "bus"},
        {"id": 105, "route_id": "route_1", "from": "بحري", "to": "شندي", "vehicle_type": "دفار سعة (نقل بضائع وعفش)", "time": "10:00 صباحاً", "seat_price": 75000, "full_price": 75000, "capacity": 1, "booked": 0, "station": "منطقة الشحن والطرود - بحري", "tickets": [], "type_key": "truck"},

        # بحري - عطبرة والعكس
        {"id": 201, "route_id": "route_2", "from": "بحري", "to": "عطبرة", "vehicle_type": "ليموزين فاخرة (4 ركاب)", "time": "07:00 صباحاً", "seat_price": 45000, "full_price": 180000, "capacity": 4, "booked": 2, "station": "موقف عطبرة - بحري", "tickets": ["WSL-2011"], "type_key": "limo"},
        {"id": 202, "route_id": "route_2", "from": "بحري", "to": "عطبرة", "vehicle_type": "بكسي دبل كاب خاص (4 ركاب)", "time": "08:00 صباحاً", "seat_price": 42000, "full_price": 165000, "capacity": 4, "booked": 1, "station": "موقف عطبرة - بحري", "tickets": [], "type_key": "pickup"},
        {"id": 203, "route_id": "route_2", "from": "بحري", "to": "عطبرة", "vehicle_type": "شريحة تويوتا (17 راكب)", "time": "09:00 صباحاً", "seat_price": 30000, "full_price": 450000, "capacity": 17, "booked": 8, "station": "موقف عطبرة - بحري", "tickets": [], "type_key": "van"},
        {"id": 204, "route_id": "route_2", "from": "بحري", "to": "عطبرة", "vehicle_type": "باص سفري فاخر (45 راكب)", "time": "06:30 صباحاً", "seat_price": 22000, "full_price": 850000, "capacity": 45, "booked": 25, "station": "الميناء البري - بحري", "tickets": [], "type_key": "bus"},
        {"id": 205, "route_id": "route_2", "from": "بحري", "to": "عطبرة", "vehicle_type": "دفار سعة (نقل بضائع وعفش)", "time": "11:00 صباحاً", "seat_price": 110000, "full_price": 110000, "capacity": 1, "booked": 0, "station": "موقف الشحن البري - بحري", "tickets": [], "type_key": "truck"},

        # بحري - مروي - كريمة والعكس
        {"id": 301, "route_id": "route_3", "from": "بحري", "to": "مروي - كريمة", "vehicle_type": "ليموزين فاخرة (4 ركاب)", "time": "06:00 صباحاً", "seat_price": 60000, "full_price": 240000, "capacity": 4, "booked": 1, "station": "الميناء البري - بحري", "tickets": [], "type_key": "limo"},
        {"id": 302, "route_id": "route_3", "from": "بحري", "to": "مروي - كريمة", "vehicle_type": "بكسي دبل كاب خاص (4 ركاب)", "time": "06:30 صباحاً", "seat_price": 58000, "full_price": 230000, "capacity": 4, "booked": 0, "station": "الميناء البري - بحري", "tickets": [], "type_key": "pickup"},
        {"id": 303, "route_id": "route_3", "from": "بحري", "to": "مروي - كريمة", "vehicle_type": "شريحة تويوتا (17 راكب)", "time": "07:00 صباحاً", "seat_price": 42000, "full_price": 600000, "capacity": 17, "booked": 12, "station": "الميناء البري - بحري", "tickets": [], "type_key": "van"},
        {"id": 304, "route_id": "route_3", "from": "بحري", "to": "مروي - كريمة", "vehicle_type": "باص سفري فاخر (45 راكب)", "time": "07:30 صباحاً", "seat_price": 32000, "full_price": 1200000, "capacity": 45, "booked": 30, "station": "الميناء البري - بحري", "tickets": [], "type_key": "bus"},
        {"id": 305, "route_id": "route_3", "from": "بحري", "to": "مروي - كريمة", "vehicle_type": "دفار سعة (نقل بضائع وعفش)", "time": "09:00 صباحاً", "seat_price": 140000, "full_price": 140000, "capacity": 1, "booked": 0, "station": "سوق الشحن البري - بحري", "tickets": [], "type_key": "truck"}
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة واصل - لخدمات السفر والليموزين والشحن</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        wasilNavy: '#0B2545',
                        wasilOrange: '#FF6B00',
                        wasilCyan: '#00A8FF',
                        wasilBg: '#F4F7FA'
                    },
                    fontFamily: { cairo: ['Cairo', 'sans-serif'] }
                }
            }
        }
    </script>
</head>
<body class="bg-wasilBg font-cairo text-gray-800 min-h-screen flex flex-col">

    <!-- Wasel Today Banner -->
    <div class="bg-gradient-to-r from-wasilNavy via-slate-800 to-wasilNavy text-white py-2 px-4 text-center text-xs flex justify-between items-center border-b border-orange-500/40 shadow-sm">
        <span class="bg-wasilOrange text-white px-2.5 py-0.5 rounded-lg text-[11px] font-black tracking-wide shadow-sm flex items-center gap-1">
            <i class="fa-solid fa-bullhorn"></i> واصل اليوم
        </span>
        <marquee id="marqueeText" class="mx-4 font-bold text-wasilCyan text-xs" scrollamount="5">
            {{ announcement }}
        </marquee>
        <span class="text-[10px] text-gray-300 hidden md:inline font-bold"><i class="fa-solid fa-headset text-wasilOrange"></i> الدعم: 0912345678</span>
    </div>

    <!-- Header -->
    <header class="bg-wasilNavy text-white shadow-xl sticky top-0 z-40">
        <div class="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
            
            <div class="flex items-center gap-3 cursor-pointer" onclick="showSection('tripsHome')">
                <div class="w-11 h-11 bg-gradient-to-tr from-wasilOrange to-amber-400 rounded-2xl flex items-center justify-center font-black text-2xl text-white shadow-lg border-2 border-white/20">
                    و
                </div>
                <div>
                    <div class="flex items-center gap-1.5">
                        <span class="text-2xl font-black text-white">واصِـل</span>
                        <span class="bg-wasilCyan text-wasilNavy text-[10px] font-bold px-1.5 py-0.5 rounded">WASIL</span>
                    </div>
                    <p class="text-[10px] text-gray-300">الليموزين والرحلات والنقل بين المدن</p>
                </div>
            </div>

            <div class="flex items-center gap-2">
                <button onclick="showSection('dailyScheduleSection')" class="bg-slate-800 hover:bg-slate-700 text-wasilCyan border border-wasilCyan/40 text-xs px-3 py-2 rounded-xl font-bold transition flex items-center gap-1">
                    <i class="fa-solid fa-calendar-days"></i> <span class="hidden sm:inline">جدول الرحلات</span>
                </button>
                <button onclick="showSection('driversSection')" class="bg-slate-800 hover:bg-slate-700 text-amber-400 border border-amber-400/40 text-xs px-3 py-2 rounded-xl font-bold transition flex items-center gap-1">
                    <i class="fa-solid fa-id-card"></i> <span class="hidden sm:inline">السائقين</span>
                </button>
                <button onclick="showSection('adminAuthSection')" class="bg-wasilOrange hover:bg-orange-600 text-white text-xs px-3 py-2 rounded-xl font-bold shadow-md transition flex items-center gap-1">
                    <i class="fa-solid fa-user-gear"></i> <span>الإدارة والمدير</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow max-w-5xl w-full mx-auto p-4 space-y-6">

        <!-- Universal Back Button -->
        <div id="backButtonBar" class="hidden flex justify-between items-center bg-white p-3 rounded-xl shadow-sm border border-gray-100">
            <button onclick="goBack()" class="bg-gray-100 hover:bg-gray-200 text-wasilNavy font-bold text-xs px-4 py-2 rounded-lg flex items-center gap-2 transition">
                <i class="fa-solid fa-arrow-right"></i> رجوع للرئيسية
            </button>
            <span id="currentPageTitle" class="text-xs font-bold text-gray-500">منصة واصل</span>
        </div>

        <!-- 1. Customer Reg Screen -->
        <section id="authSection" class="max-w-md mx-auto my-6 bg-white p-6 rounded-2xl shadow-xl border border-gray-100">
            <div class="text-center mb-6">
                <div class="w-16 h-16 bg-orange-100 text-wasilOrange rounded-full flex items-center justify-center mx-auto mb-3 text-3xl shadow-inner">
                    <i class="fa-solid fa-ticket"></i>
                </div>
                <h2 class="text-2xl font-black text-wasilNavy">حجز التذاكر والرحلات - واصل</h2>
                <p class="text-xs text-gray-500 mt-1">أنشئ حسابك للوصول المباشر للرحلات اليومية</p>
            </div>

            <form onsubmit="handleUserAuth(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1">الاسم بالكامل</label>
                    <input type="text" id="custName" required placeholder="أدخل اسمك الكريم" class="w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-wasilOrange outline-none text-sm bg-gray-50/50">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1">رقم الهاتف</label>
                    <input type="tel" id="custPhone" required placeholder="09xxxxxxx" class="w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-wasilOrange outline-none text-sm bg-gray-50/50">
                </div>
                <button type="submit" class="w-full bg-wasilOrange hover:bg-orange-600 text-white font-bold py-3.5 rounded-xl shadow-lg transition text-sm">
                    إنشاء حساب والدخول لشراء التذاكر
                </button>
            </form>

            <div class="relative my-6 text-center">
                <hr class="border-gray-200">
                <span class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white px-3 text-xs text-gray-400 font-bold">أو</span>
            </div>

            <button onclick="directUserLogin()" class="w-full bg-slate-100 hover:bg-slate-200 text-wasilNavy font-bold py-3 rounded-xl transition text-xs flex items-center justify-center gap-2">
                <i class="fa-solid fa-right-to-bracket text-wasilCyan"></i> لدي حساب بالفعل (دخول تلقائي)
            </button>
        </section>

        <!-- 2. Routes Selection Section -->
        <section id="tripsHome" class="hidden space-y-6">
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex justify-between items-center flex-wrap gap-2">
                <div>
                    <span class="text-xs text-gray-400 block">أهلاً بك عزيزي المسافر:</span>
                    <h3 id="loggedUserName" class="font-black text-wasilNavy text-base">مسافر واصل</h3>
                </div>
                <span class="bg-blue-50 text-wasilCyan border border-wasilCyan/30 text-xs px-3 py-1.5 rounded-xl font-bold">
                    <i class="fa-solid fa-route"></i> اختر المدينة والوجهة
                </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div onclick="selectRoute('route_1', 'بحري - شندي والعكس')" class="bg-white hover:border-wasilOrange border-2 border-transparent p-5 rounded-2xl shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="w-12 h-12 bg-orange-100 text-wasilOrange rounded-xl flex items-center justify-center text-xl font-bold mb-3 group-hover:scale-110 transition"><i class="fa-solid fa-location-dot"></i></div>
                    <h4 class="font-extrabold text-wasilNavy text-lg mb-1">بحري <i class="fa-solid fa-arrow-right-left text-xs text-wasilCyan mx-1"></i> شندي</h4>
                    <p class="text-xs text-gray-500 mb-3">ليموزين، بكسي خاص، شريحة، باص، ودفار سعة</p>
                    <span class="text-xs text-wasilOrange font-bold">عرض وسائل النقل الـ 5 <i class="fa-solid fa-chevron-left text-[10px]"></i></span>
                </div>

                <div onclick="selectRoute('route_2', 'بحري - عطبرة والعكس')" class="bg-white hover:border-wasilOrange border-2 border-transparent p-5 rounded-2xl shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="w-12 h-12 bg-blue-100 text-wasilCyan rounded-xl flex items-center justify-center text-xl font-bold mb-3 group-hover:scale-110 transition"><i class="fa-solid fa-building-flag"></i></div>
                    <h4 class="font-extrabold text-wasilNavy text-lg mb-1">بحري <i class="fa-solid fa-arrow-right-left text-xs text-wasilCyan mx-1"></i> عطبرة</h4>
                    <p class="text-xs text-gray-500 mb-3">ليموزين، بكسي خاص، شريحة، باص، ودفار سعة</p>
                    <span class="text-xs text-wasilOrange font-bold">عرض وسائل النقل الـ 5 <i class="fa-solid fa-chevron-left text-[10px]"></i></span>
                </div>

                <div onclick="selectRoute('route_3', 'بحري - مروي - كريمة والعكس')" class="bg-white hover:border-wasilOrange border-2 border-transparent p-5 rounded-2xl shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="w-12 h-12 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center text-xl font-bold mb-3 group-hover:scale-110 transition"><i class="fa-solid fa-mountain-sun"></i></div>
                    <h4 class="font-extrabold text-wasilNavy text-lg mb-1">بحري <i class="fa-solid fa-arrow-right-left text-xs text-wasilCyan mx-1"></i> مروي - كريمة</h4>
                    <p class="text-xs text-gray-500 mb-3">ليموزين، بكسي خاص، شريحة، باص، ودفار سعة</p>
                    <span class="text-xs text-wasilOrange font-bold">عرض وسائل النقل الـ 5 <i class="fa-solid fa-chevron-left text-[10px]"></i></span>
                </div>
            </div>
        </section>

        <!-- 3. Vehicles Section -->
        <section id="vehiclesSection" class="hidden space-y-4">
            <div class="bg-wasilNavy text-white p-5 rounded-2xl shadow-md flex justify-between items-center">
                <div>
                    <span class="text-xs text-wasilOrange font-bold block">الخط المحدد للرحلات:</span>
                    <h3 id="selectedRouteName" class="text-xl font-black"></h3>
                </div>
                <button onclick="goBack()" class="bg-white/10 hover:bg-white/20 text-white text-xs px-3 py-1.5 rounded-lg border border-white/20">تغيير الوجهة</button>
            </div>

            <!-- Vehicle Filter Tabs -->
            <div class="flex gap-2 overflow-x-auto pb-2 text-xs font-bold">
                <button onclick="filterVehicles('all')" id="vFilter_all" class="px-3.5 py-2 bg-wasilNavy text-white rounded-xl shadow whitespace-nowrap">الكل (5 وسائل)</button>
                <button onclick="filterVehicles('limo')" id="vFilter_limo" class="px-3.5 py-2 bg-white text-gray-700 border hover:border-wasilOrange rounded-xl whitespace-nowrap"><i class="fa-solid fa-car-side text-wasilOrange"></i> ليموزين فاخرة</button>
                <button onclick="filterVehicles('pickup')" id="vFilter_pickup" class="px-3.5 py-2 bg-white text-gray-700 border hover:border-wasilOrange rounded-xl whitespace-nowrap"><i class="fa-solid fa-truck-pickup text-wasilOrange"></i> بكسي دبل كاب</button>
                <button onclick="filterVehicles('van')" id="vFilter_van" class="px-3.5 py-2 bg-white text-gray-700 border hover:border-wasilOrange rounded-xl whitespace-nowrap"><i class="fa-solid fa-van-shuttle text-wasilOrange"></i> شريحة (17 راكب)</button>
                <button onclick="filterVehicles('bus')" id="vFilter_bus" class="px-3.5 py-2 bg-white text-gray-700 border hover:border-wasilOrange rounded-xl whitespace-nowrap"><i class="fa-solid fa-bus-simple text-wasilOrange"></i> باص (45 راكب)</button>
                <button onclick="filterVehicles('truck')" id="vFilter_truck" class="px-3.5 py-2 bg-white text-gray-700 border hover:border-wasilOrange rounded-xl whitespace-nowrap"><i class="fa-solid fa-truck-moving text-wasilOrange"></i> دفار سعة (شحن)</button>
            </div>

            <div id="routeTripsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        </section>

        <!-- 4. Daily Schedule Screen -->
        <section id="dailyScheduleSection" class="hidden space-y-4">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <h3 class="text-lg font-black text-wasilNavy mb-4"><i class="fa-solid fa-clock text-wasilCyan"></i> جدول الرحلات اليومية وأزمنة القيام وقيمة التذاكر</h3>
                <div id="fullScheduleContainer" class="space-y-3"></div>
            </div>
        </section>

        <!-- 5. Drivers Data -->
        <section id="driversSection" class="hidden space-y-4">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <h3 class="text-xl font-black text-wasilNavy mb-4"><i class="fa-solid fa-id-card text-wasilOrange"></i> السائقين والسيارات المعتمدة والدفارات</h3>
                <div id="driversListCards" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
            </div>
        </section>

        <!-- 6. Admin Auth Screen -->
        <section id="adminAuthSection" class="hidden max-w-md mx-auto my-6 bg-white p-6 rounded-2xl shadow-xl border border-gray-100">
            <div class="text-center mb-6">
                <div class="w-14 h-14 bg-wasilNavy text-amber-400 rounded-full flex items-center justify-center mx-auto mb-2 text-2xl shadow-md">
                    <i class="fa-solid fa-user-shield"></i>
                </div>
                <h3 class="text-xl font-black text-wasilNavy">بوابة المدير والمشرفين الإثنين</h3>
                <p class="text-xs text-gray-500">سجل دخولك بالرقم السري الخاص بحسابك</p>
            </div>

            <form onsubmit="handleAdminLogin(event)" class="space-y-4 text-xs font-bold">
                <div>
                    <label class="block text-gray-700 mb-1">اختر الحساب المطلوب:</label>
                    <select id="adminUserSelect" class="w-full p-3 border rounded-xl bg-gray-50 outline-none text-wasilNavy font-bold">
                        <option value="admin">1. المدير العام (صلاحيات كاملة)</option>
                        <option value="sup1">2. عمر خالد (مشرف حركة الرحلات والمواقف)</option>
                        <option value="sup2">3. ياسر عثمان (مشرف الشركات والدفارات والسائقين)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-gray-700 mb-1">كلمة المرور (Password)</label>
                    <input type="password" id="adminPassInput" required placeholder="أدخل كلمة المرور" class="w-full p-3 border rounded-xl outline-none focus:ring-2 focus:ring-wasilOrange">
                    <span class="text-[10px] text-gray-400 block mt-1">كلمة المرور للمدير: admin123 | للمشرفين: sup123 أو sup223</span>
                </div>
                <button type="submit" class="w-full bg-wasilNavy hover:bg-slate-800 text-white font-bold py-3 rounded-xl shadow transition text-sm">
                    تسجيل الدخول للنظام
                </button>
            </form>
        </section>

        <!-- 7. Admin Dashboard -->
        <section id="adminDashboard" class="hidden space-y-6">
            <div class="bg-wasilNavy text-white p-6 rounded-2xl shadow-lg flex justify-between items-center flex-wrap gap-2">
                <div>
                    <span id="activeRoleTitle" class="bg-wasilOrange text-white text-[10px] font-bold px-2.5 py-0.5 rounded-full">المدير العام</span>
                    <h2 class="text-xl font-black mt-1">لوحة الإدارة والتحكم - واصل</h2>
                </div>
                <button onclick="showSection('tripsHome')" class="bg-white/10 hover:bg-white/20 text-white text-xs px-3 py-2 rounded-xl border border-white/20">
                    <i class="fa-solid fa-arrow-right"></i> خروج للموقع
                </button>
            </div>

            <!-- Sub Navigation Tabs -->
            <div class="flex gap-2 border-b border-gray-200 pb-2 overflow-x-auto text-xs font-bold">
                <button onclick="switchAdminTab('accountTab')" class="px-4 py-2 bg-wasilOrange text-white rounded-xl shadow" id="tabBtn_account">
                    <i class="fa-solid fa-user-gear"></i> بيانات الحساب والإعلان
                </button>
                <button onclick="switchAdminTab('companiesTab')" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-xl" id="tabBtn_companies">
                    <i class="fa-solid fa-building"></i> إدارة شركات النقل
                </button>
                <button onclick="switchAdminTab('staffTripsTab')" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-xl" id="tabBtn_staffTrips">
                    <i class="fa-solid fa-bus"></i> متابعة التذاكر والدفارات
                </button>
            </div>

            <!-- TAB 1: Account & Announcement Live Control -->
            <div id="adminTab_account" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-6">
                
                <!-- Live Announcement Edit Box -->
                <div class="bg-orange-50/70 border border-orange-200 p-4 rounded-2xl space-y-3">
                    <div class="flex justify-between items-center">
                        <h4 class="font-black text-wasilNavy text-sm flex items-center gap-2">
                            <i class="fa-solid fa-bullhorn text-wasilOrange"></i> تعديل نص شريط الإعلانات العريض (واصل اليوم)
                        </h4>
                        <span class="bg-wasilOrange text-white text-[10px] font-bold px-2 py-0.5 rounded">خاص بالمدير</span>
                    </div>
                    <div class="flex gap-2">
                        <input type="text" id="announcementInput" placeholder="أدخل نص إعلان واصل اليوم الجديد..." class="w-full p-3 border rounded-xl text-xs bg-white font-bold outline-none">
                        <button onclick="updateAnnouncement()" class="bg-wasilOrange hover:bg-orange-600 text-white font-bold px-4 rounded-xl text-xs shadow whitespace-nowrap">
                            تحديث الإعلان الآن
                        </button>
                    </div>
                </div>

                <div class="border-b pb-4">
                    <h3 class="text-lg font-black text-wasilNavy"><i class="fa-solid fa-id-card-clip text-wasilOrange"></i> تعديل بيانات الحساب وكلمة المرور</h3>
                </div>

                <div class="space-y-4 text-xs font-bold">
                    <div class="flex items-center gap-4 bg-gray-50 p-4 rounded-xl border">
                        <img id="editUserPhotoPreview" src="" class="w-16 h-16 rounded-full object-cover border-2 border-wasilOrange">
                        <div>
                            <h4 id="editUserRoleName" class="text-sm font-black text-wasilNavy"></h4>
                            <span id="editUserUsername" class="text-gray-400 text-[11px]"></span>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-gray-700 mb-1">الاسم الكامل</label>
                            <input type="text" id="editName" class="w-full p-2.5 border rounded-xl bg-white">
                        </div>
                        <div>
                            <label class="block text-gray-700 mb-1">رقم الهاتف</label>
                            <input type="text" id="editPhone" class="w-full p-2.5 border rounded-xl bg-white">
                        </div>
                        <div>
                            <label class="block text-gray-700 mb-1">رقم الهوية الوطنية</label>
                            <input type="text" id="editNationalId" class="w-full p-2.5 border rounded-xl bg-white">
                        </div>
                        <div>
                            <label class="block text-gray-700 mb-1">رابط الصورة الشخصية</label>
                            <input type="text" id="editPhotoUrl" class="w-full p-2.5 border rounded-xl bg-white">
                        </div>
                        <div class="md:col-span-2 bg-orange-50/60 p-3 rounded-xl border border-orange-200">
                            <label class="block text-wasilOrange font-black mb-1"><i class="fa-solid fa-key"></i> كلمة المرور الجديدة (Password)</label>
                            <input type="password" id="editPassword" class="w-full p-2.5 border rounded-xl bg-white">
                        </div>
                    </div>

                    <!-- Security Pledge -->
                    <div class="bg-red-50/80 border border-red-200 p-4 rounded-xl space-y-2 text-red-900">
                        <h5 class="font-extrabold flex items-center gap-1.5"><i class="fa-solid fa-shield-halved text-red-600"></i> التعهد الأمني بعدم تسريب المعلومات:</h5>
                        <p class="text-[11px] leading-relaxed text-gray-700">
                            "أتعهد أنا صاحب هذا الحساب بالمحافظة التامة على سرية بيانات رحلات المسافرين وإحصائيات شركات النقل والدفارات، وأتعهد بعدم تسريبها أو المتاجرة بها بأي شكل كان."
                        </p>
                        <div class="flex items-center gap-2 pt-1">
                            <input type="checkbox" id="pledgeCheck" class="w-4 h-4 text-wasilOrange rounded border-gray-300">
                            <label for="pledgeCheck" class="font-bold text-xs text-red-800 cursor-pointer">أوافق وأتعهد بالالتزام بالسرية</label>
                        </div>
                    </div>

                    <button onclick="saveProfileChanges()" class="bg-wasilNavy hover:bg-slate-800 text-white font-bold px-6 py-3 rounded-xl shadow text-xs transition flex items-center gap-2">
                        <i class="fa-solid fa-floppy-disk"></i> حفظ كلمة المرور والتغييرات
                    </button>
                </div>
            </div>

            <!-- TAB 2: Companies Tab -->
            <div id="adminTab_companies" class="hidden bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-6">
                <div class="border-b pb-4">
                    <h3 class="text-base font-black text-wasilNavy mb-2"><i class="fa-solid fa-plus-circle text-wasilOrange"></i> تسجيل شركة نقل جديدة</h3>
                    <form onsubmit="addNewCompany(event)" class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <input type="text" id="newCompName" required placeholder="اسم شركة النقل" class="p-3 border rounded-xl">
                        <input type="text" id="newCompPhone" required placeholder="رقم الاتصال والتواصل" class="p-3 border rounded-xl">
                        <input type="url" id="newCompWebsite" placeholder="العنوان أو الصفحة الإلكترونية (https://...)" class="p-3 border rounded-xl">
                        <button type="submit" class="bg-wasilOrange hover:bg-orange-600 text-white font-bold p-3 rounded-xl shadow transition md:col-span-3">
                            إضافة الشركة
                        </button>
                    </form>
                </div>

                <div class="space-y-3">
                    <h4 class="font-extrabold text-wasilNavy text-sm"><i class="fa-solid fa-list-check text-wasilCyan"></i> قائمة شركات النقل المسجلة والمعروضة بالمنصة:</h4>
                    <div class="overflow-x-auto">
                        <table class="w-full text-right text-xs">
                            <thead class="bg-gray-100 text-gray-700 font-bold border-b">
                                <tr>
                                    <th class="p-3">اسم الشركة</th>
                                    <th class="p-3">رقم الهاتف والتواصل</th>
                                    <th class="p-3">العنوان / الصفحة الإلكترونية</th>
                                    <th class="p-3 text-center">الإجراء</th>
                                </tr>
                            </thead>
                            <tbody id="companiesTableBody"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 3: Internal Staff Trips Monitor -->
            <div id="adminTab_staffTrips" class="hidden bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-4">
                <h4 class="font-extrabold text-wasilNavy text-sm"><i class="fa-solid fa-eye text-wasilOrange"></i> متابعة أعداد الركاب والتذاكر والدفارات المحجوزة لكل مدينة</h4>
                <div class="overflow-x-auto">
                    <table class="w-full text-right text-xs">
                        <thead class="bg-gray-100 text-gray-700 font-bold border-b">
                            <tr>
                                <th class="p-3">رقم الرحلة</th>
                                <th class="p-3">الخط والجهة</th>
                                <th class="p-3">وسيلة النقل</th>
                                <th class="p-3">الركاب / السعة المتبقية</th>
                                <th class="p-3">أرقام التذاكر المحجوزة</th>
                            </tr>
                        </thead>
                        <tbody id="internalStaffTable"></tbody>
                    </table>
                </div>
            </div>
        </section>

    </main>

    <!-- Booking Options & Payment Modal -->
    <div id="bookingModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm hidden z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
            <button onclick="closeBookingModal()" class="absolute top-4 left-4 text-gray-400 hover:text-gray-600"><i class="fa-solid fa-xmark text-xl"></i></button>

            <!-- Step 1: Booking & Payment Options Form -->
            <div id="paymentStep">
                <div class="text-center mb-4">
                    <div class="w-12 h-12 bg-orange-100 text-wasilOrange rounded-full flex items-center justify-center mx-auto mb-2 text-2xl"><i class="fa-solid fa-receipt"></i></div>
                    <h3 class="font-extrabold text-lg text-wasilNavy">خيارات الحجز والدفع - واصل</h3>
                    <p class="text-xs text-gray-500" id="modalVehicleTitle"></p>
                </div>

                <form onsubmit="confirmBooking(event)" class="space-y-4 text-xs">
                    
                    <!-- Passenger Booking Options (Limo, Pickup, Van, Bus) -->
                    <div id="passengerBookingOptions" class="space-y-3">
                        <div>
                            <label class="block font-extrabold text-gray-700 mb-1">نوع الحجز المطلوب:</label>
                            <select id="bookingTypeSelect" onchange="updatePriceDisplay()" class="w-full p-3 border rounded-xl font-bold text-wasilNavy bg-gray-50 outline-none">
                                <option value="seat">حجز تذكرة مقعد فردي</option>
                                <option value="full">حجز كامل للمركبة (سيارة خاصة / إيجار)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Dafar Freight Options (For Truck only) -->
                    <div id="dafarBookingOptions" class="hidden space-y-3 bg-amber-50/70 p-3 rounded-xl border border-amber-200">
                        <div>
                            <label class="block font-bold text-gray-800 mb-1">نوع الشحنة / العفش:</label>
                            <input type="text" id="dafarCargoType" placeholder="مثال: أثاث منزل، طرود، مواد تجارية..." class="w-full p-2.5 border rounded-xl bg-white outline-none">
                        </div>
                        <div>
                            <label class="block font-bold text-gray-800 mb-1">الوزن / الحجم المقدر:</label>
                            <input type="text" id="dafarWeight" placeholder="مثال: 3 طن / حمولة كاملة" class="w-full p-2.5 border rounded-xl bg-white outline-none">
                        </div>
                        
                        <!-- Dafar Legal Pledge Checkbox -->
                        <div class="bg-red-50 border border-red-200 p-2.5 rounded-xl space-y-1 text-red-900">
                            <div class="flex items-start gap-2">
                                <input type="checkbox" id="dafarLegalPledge" class="w-4 h-4 text-wasilOrange rounded mt-0.5">
                                <label for="dafarLegalPledge" class="font-bold text-[10px] leading-relaxed cursor-pointer">
                                    أتعهد بأن جميع تصاديق الطريق ورسوم العبور على صاحب البضاعة، وأي مخالفة قانونية في العفش/البضائع يتحمل مسئوليتها صاحب البضائع بالكامل.
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Payment Method Options -->
                    <div>
                        <label class="block font-extrabold text-gray-700 mb-1">طريقة الدفع والسداد:</label>
                        <select id="paymentMethodSelect" onchange="togglePaymentFields()" class="w-full p-3 border rounded-xl font-bold text-wasilNavy bg-gray-50 outline-none">
                            <option value="bankak">تطبيق بنكك (رقم الحساب: 9824691)</option>
                            <option value="cash">دفع كاش بالمكتب (عند الحضور)</option>
                        </select>
                    </div>

                    <!-- Bankak Info & OTP Box -->
                    <div id="bankakDetailsBox" class="bg-amber-50 border border-amber-200 p-3 rounded-xl space-y-2">
                        <div class="flex justify-between font-bold">
                            <span class="text-gray-700">رقم حساب بنكك المعتمد:</span> 
                            <span class="text-wasilOrange text-sm font-black tracking-wider">9824691</span>
                        </div>
                        <div class="flex justify-between text-[11px]">
                            <span class="text-gray-500">اسم الحساب:</span> 
                            <span class="font-bold">شركة واصل لخدمات النقل</span>
                        </div>
                        <div>
                            <label class="block font-bold text-gray-700 mb-1">رمز التحقق OTP أو رقم العملية:</label>
                            <input type="text" id="modalOtpInput" placeholder="أدخل رمز OTP البنك" class="w-full p-2.5 border rounded-xl text-center text-sm font-bold tracking-widest bg-white outline-none">
                        </div>
                    </div>

                    <!-- Cash Notice Box -->
                    <div id="cashDetailsBox" class="hidden bg-blue-50 border border-blue-200 p-3 rounded-xl text-blue-900 text-xs leading-relaxed font-semibold">
                        <i class="fa-solid fa-store text-wasilCyan"></i> يتم السداد نقداً (كاش) في مكتب منصة واصل المعتمد بالموقف قبل موعد انطلاق الرحلة.
                    </div>

                    <!-- Price Display Summary -->
                    <div class="bg-gray-100 p-3 rounded-xl flex justify-between items-center font-black">
                        <span class="text-gray-600">المبلغ الإجمالي المطلـوب:</span>
                        <span id="modalFinalPrice" class="text-wasilOrange text-base"></span>
                    </div>

                    <button type="submit" class="w-full bg-wasilOrange hover:bg-orange-600 text-white font-bold py-3.5 rounded-xl shadow transition text-sm flex items-center justify-center gap-2">
                        <i class="fa-solid fa-circle-check"></i> تأكيد الحجز وإصدار التذكرة
                    </button>
                </form>
            </div>

            <!-- Step 2: Generated E-Ticket Result View with QR Code -->
            <div id="ticketResultStep" class="hidden">
                <div class="border-2 border-dashed border-wasilNavy p-4 rounded-2xl bg-orange-50/20 text-center relative">
                    <div class="flex justify-between items-center border-b pb-2 mb-3">
                        <div class="flex items-center gap-1">
                            <span class="w-6 h-6 bg-wasilOrange text-white rounded-lg flex items-center justify-center text-xs font-black">و</span>
                            <span class="font-black text-wasilNavy text-base">تذكرة إلكترونية - واصل</span>
                        </div>
                        <span id="tktPaymentBadge" class="bg-green-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-full">مدفوعة - بنكك</span>
                    </div>

                    <div class="space-y-2 text-right text-xs">
                        <div class="flex justify-between"><span class="text-gray-500">رقم التذكرة:</span> <span id="tktNo" class="font-extrabold text-wasilOrange"></span></div>
                        <div class="flex justify-between"><span class="text-gray-500">اسم المسافر/الشاحن:</span> <span id="tktPassenger" class="font-bold"></span></div>
                        <div class="flex justify-between"><span class="text-gray-500">الوجهة والخط:</span> <span id="tktRoute" class="font-bold text-wasilNavy"></span></div>
                        <div class="flex justify-between"><span class="text-gray-500">نوع الحجز:</span> <span id="tktBookingType" class="font-bold text-wasilCyan"></span></div>
                        <div class="flex justify-between"><span class="text-gray-500">زمن القيام:</span> <span id="tktTime" class="font-bold"></span></div>
                        <div class="flex justify-between"><span class="text-gray-500">مكان الانطلاق:</span> <span id="tktStation" class="font-bold text-gray-800"></span></div>
                    </div>

                    <!-- QR Code Generated Image -->
                    <div class="mt-4 pt-3 border-t flex flex-col items-center">
                        <img id="tktQrImage" src="" class="w-28 h-28 border p-1 bg-white rounded-lg shadow-sm mb-1">
                        <span class="text-[9px] text-gray-400 font-bold">امسح الكود إلكترونياً عند الصعود بالمكتب</span>
                    </div>
                </div>

                <button onclick="closeBookingModal()" class="w-full mt-4 bg-wasilNavy text-white font-bold py-2.5 rounded-xl text-xs">تم / العودة للرحلات</button>
            </div>
        </div>
    </div>

    <!-- JavaScript Logic -->
    <script>
        let currentUser = { name: "مسافر واصل", phone: "" };
        let activeAdminUser = null;
        let selectedTripForBooking = null;
        let currentRouteTrips = [];

        function showSection(sectionId) {
            ['authSection', 'tripsHome', 'vehiclesSection', 'dailyScheduleSection', 'driversSection', 'adminAuthSection', 'adminDashboard'].forEach(id => {
                document.getElementById(id).classList.add('hidden');
            });

            document.getElementById(sectionId).classList.remove('hidden');

            const backBar = document.getElementById('backButtonBar');
            if(sectionId !== 'authSection' && sectionId !== 'tripsHome') {
                backBar.classList.remove('hidden');
            } else {
                backBar.classList.add('hidden');
            }

            if(sectionId === 'dailyScheduleSection') loadFullDailySchedule();
            if(sectionId === 'driversSection') loadDriversData();
        }

        function goBack() { showSection('tripsHome'); }

        function handleUserAuth(e) {
            e.preventDefault();
            const name = document.getElementById('custName').value;
            const phone = document.getElementById('custPhone').value;
            if(name && phone) {
                currentUser = { name, phone };
                document.getElementById('loggedUserName').innerText = name;
                showSection('tripsHome');
            }
        }

        function directUserLogin() {
            currentUser = { name: "مسافر واصل", phone: "09xxxxxxx" };
            document.getElementById('loggedUserName').innerText = currentUser.name;
            showSection('tripsHome');
        }

        function selectRoute(routeId, routeName) {
            document.getElementById('selectedRouteName').innerText = routeName;
            showSection('vehiclesSection');

            fetch('/api/trips')
                .then(res => res.json())
                .then(trips => {
                    currentRouteTrips = trips.filter(t => t.route_id === routeId);
                    renderVehicleCards(currentRouteTrips);
                });
        }

        function filterVehicles(typeKey) {
            ['all', 'limo', 'pickup', 'van', 'bus', 'truck'].forEach(k => {
                const btn = document.getElementById(`vFilter_${k}`);
                if(btn) btn.className = "px-3.5 py-2 bg-white text-gray-700 border hover:border-wasilOrange rounded-xl whitespace-nowrap";
            });
            const activeBtn = document.getElementById(`vFilter_${typeKey}`);
            if(activeBtn) activeBtn.className = "px-3.5 py-2 bg-wasilNavy text-white rounded-xl shadow whitespace-nowrap";

            if(typeKey === 'all') {
                renderVehicleCards(currentRouteTrips);
            } else {
                const filtered = currentRouteTrips.filter(t => t.type_key === typeKey);
                renderVehicleCards(filtered);
            }
        }

        function renderVehicleCards(trips) {
            const container = document.getElementById('routeTripsList');
            container.innerHTML = '';

            if(trips.length === 0) {
                container.innerHTML = `<div class="col-span-3 text-center p-8 bg-white rounded-xl text-gray-400 font-bold">لا توجد رحلات حالياً.</div>`;
                return;
            }

            trips.forEach(trip => {
                const remaining = trip.capacity - trip.booked;
                let icon = 'fa-car-side';
                if(trip.type_key === 'pickup') icon = 'fa-truck-pickup';
                if(trip.type_key === 'van') icon = 'fa-van-shuttle';
                if(trip.type_key === 'bus') icon = 'fa-bus-simple';
                if(trip.type_key === 'truck') icon = 'fa-truck-moving';

                const isTruck = trip.type_key === 'truck';

                container.innerHTML += `
                    <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition">
                        <div>
                            <div class="flex justify-between items-center mb-3">
                                <span class="bg-orange-50 text-wasilOrange font-extrabold text-xs px-2.5 py-1 rounded-lg flex items-center gap-1">
                                    <i class="fa-solid ${icon}"></i> ${trip.vehicle_type}
                                </span>
                            </div>
                            <h4 class="font-extrabold text-gray-800 text-sm mb-2">${trip.from} إلى ${trip.to}</h4>
                            <div class="text-xs text-gray-600 space-y-1 mb-4 bg-gray-50 p-2.5 rounded-xl border">
                                ${isTruck ? `
                                    <div><i class="fa-solid fa-truck-moving text-wasilOrange"></i> تكلفة الشحن: <b class="text-wasilNavy">${trip.full_price.toLocaleString()} ج.س</b></div>
                                ` : `
                                    <div><i class="fa-solid fa-ticket text-wasilOrange"></i> سعر المقعد الفردي: <b class="text-wasilNavy">${trip.seat_price.toLocaleString()} ج.س</b></div>
                                    <div><i class="fa-solid fa-car text-wasilCyan"></i> سعر الإيجار الكامل: <b class="text-green-700">${trip.full_price.toLocaleString()} ج.س</b></div>
                                    <div><i class="fa-solid fa-chair text-green-600"></i> المقاعد المتبقية: <b class="text-green-700">${remaining} مقاعد من أصل ${trip.capacity}</b></div>
                                `}
                                <div><i class="fa-solid fa-clock text-blue-600"></i> زمن القيام: <b>${trip.time}</b></div>
                                <div><i class="fa-solid fa-location-dot text-red-500"></i> مكان الانطلاق: <b>${trip.station}</b></div>
                            </div>
                        </div>
                        <button onclick="openBookingModal(${trip.id})" class="w-full bg-wasilNavy hover:bg-slate-800 text-white font-bold py-2.5 rounded-xl text-xs transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid ${isTruck ? 'fa-box' : 'fa-ticket'}"></i> ${isTruck ? 'حجز دفار وشحن' : 'حجز تذكرة / إيجار كامل'}
                        </button>
                    </div>
                `;
            });
        }

        function openBookingModal(tripId) {
            fetch('/api/trips')
                .then(res => res.json())
                .then(trips => {
                    selectedTripForBooking = trips.find(t => t.id === tripId);
                    document.getElementById('modalVehicleTitle').innerText = `${selectedTripForBooking.vehicle_type} (${selectedTripForBooking.from} إلى ${selectedTripForBooking.to})`;

                    const isTruck = selectedTripForBooking.type_key === 'truck';
                    if(isTruck) {
                        document.getElementById('passengerBookingOptions').classList.add('hidden');
                        document.getElementById('dafarBookingOptions').classList.remove('hidden');
                    } else {
                        document.getElementById('passengerBookingOptions').classList.remove('hidden');
                        document.getElementById('dafarBookingOptions').classList.add('hidden');
                        document.getElementById('bookingTypeSelect').value = 'seat';
                    }

                    document.getElementById('paymentMethodSelect').value = 'bankak';
                    updatePriceDisplay();
                    togglePaymentFields();

                    document.getElementById('paymentStep').classList.remove('hidden');
                    document.getElementById('ticketResultStep').classList.add('hidden');
                    document.getElementById('bookingModal').classList.remove('hidden');
                });
        }

        function updatePriceDisplay() {
            if(!selectedTripForBooking) return;
            const isTruck = selectedTripForBooking.type_key === 'truck';
            if(isTruck) {
                document.getElementById('modalFinalPrice').innerText = `${selectedTripForBooking.full_price.toLocaleString()} ج.س`;
            } else {
                const bType = document.getElementById('bookingTypeSelect').value;
                const price = bType === 'full' ? selectedTripForBooking.full_price : selectedTripForBooking.seat_price;
                document.getElementById('modalFinalPrice').innerText = `${price.toLocaleString()} ج.س`;
            }
        }

        function togglePaymentFields() {
            const method = document.getElementById('paymentMethodSelect').value;
            if(method === 'bankak') {
                document.getElementById('bankakDetailsBox').classList.remove('hidden');
                document.getElementById('cashDetailsBox').classList.add('hidden');
            } else {
                document.getElementById('bankakDetailsBox').classList.add('hidden');
                document.getElementById('cashDetailsBox').classList.remove('hidden');
            }
        }

        function closeBookingModal() { document.getElementById('bookingModal').classList.add('hidden'); }

        function confirmBooking(e) {
            e.preventDefault();
            const isTruck = selectedTripForBooking.type_key === 'truck';
            let bType = 'seat';

            if(isTruck) {
                bType = 'dafar_cargo';
                const pledged = document.getElementById('dafarLegalPledge').checked;
                if(!pledged) {
                    alert('عذراً، يجب الموافقة على التعهد بأن تصاديق ومخالفات العفش على صاحب البضاعة!');
                    return;
                }
            } else {
                bType = document.getElementById('bookingTypeSelect').value;
            }

            const pMethod = document.getElementById('paymentMethodSelect').value;
            const otp = document.getElementById('modalOtpInput').value;

            if(pMethod === 'bankak' && !otp) {
                alert('الرجاء أدخل رمز OTP الخاص بعملية التحويل للبنك');
                return;
            }

            fetch('/api/book', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    tripId: selectedTripForBooking.id,
                    passengerName: currentUser.name,
                    bookingType: bType,
                    paymentMethod: pMethod
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('tktNo').innerText = data.ticketNo;
                document.getElementById('tktPassenger').innerText = currentUser.name;
                document.getElementById('tktRoute').innerText = `${selectedTripForBooking.from} إلى ${selectedTripForBooking.to}`;
                
                let bTypeTitle = 'تذكرة مقعد فردي';
                if(bType === 'full') bTypeTitle = 'حجز كامل للمركبة (خاص)';
                if(bType === 'dafar_cargo') bTypeTitle = 'حجز دفار لشحن بضائع';

                document.getElementById('tktBookingType').innerText = bTypeTitle;
                document.getElementById('tktTime').innerText = selectedTripForBooking.time;
                document.getElementById('tktStation').innerText = selectedTripForBooking.station;

                const badge = document.getElementById('tktPaymentBadge');
                if(pMethod === 'bankak') {
                    badge.innerText = 'مدفوعة - بنكك (9824691)';
                    badge.className = 'bg-green-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-full';
                } else {
                    badge.innerText = 'دفع كاش بالمكتب';
                    badge.className = 'bg-amber-500 text-white text-[9px] font-bold px-2 py-0.5 rounded-full';
                }

                // Generate QR code URL
                document.getElementById('tktQrImage').src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=WASIL_TICKET_${data.ticketNo}`;

                document.getElementById('paymentStep').classList.add('hidden');
                document.getElementById('ticketResultStep').classList.remove('hidden');

                // Refresh active trip view
                selectRoute(selectedTripForBooking.route_id, document.getElementById('selectedRouteName').innerText);
            });
        }

        function updateAnnouncement() {
            const text = document.getElementById('announcementInput').value;
            if(!text) return;

            fetch('/api/announcement/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text })
            })
            .then(res => res.json())
            .then(data => {
                alert('تم تحديث شريط إعلانات واصل اليوم بنجاح!');
                document.getElementById('marqueeText').innerText = text;
            });
        }

        function handleAdminLogin(e) {
            e.preventDefault();
            const userKey = document.getElementById('adminUserSelect').value;
            const pass = document.getElementById('adminPassInput').value;

            fetch('/api/admin/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ userKey, pass })
            })
            .then(res => res.json())
            .then(data => {
                if(data.status === 'success') {
                    activeAdminUser = data.user;
                    document.getElementById('activeRoleTitle').innerText = activeAdminUser.role_title;
                    loadProfileData();
                    showSection('adminDashboard');
                } else {
                    alert(data.message);
                }
            });
        }

        function switchAdminTab(tabName) {
            ['account', 'companies', 'staffTrips'].forEach(t => {
                document.getElementById(`adminTab_${t}`).classList.add('hidden');
                document.getElementById(`tabBtn_${t}`).className = "px-4 py-2 bg-gray-100 text-gray-700 rounded-xl";
            });
            document.getElementById(`adminTab_${tabName}`).classList.remove('hidden');
            document.getElementById(`tabBtn_${tabName}`).className = "px-4 py-2 bg-wasilOrange text-white rounded-xl shadow";

            if(tabName === 'companies') loadCompaniesTable();
            if(tabName === 'staffTrips') loadInternalStaffData();
        }

        function loadProfileData() {
            document.getElementById('editUserRoleName').innerText = activeAdminUser.name;
            document.getElementById('editUserUsername').innerText = `اسم المستخدم للنظام: ${activeAdminUser.username}`;
            document.getElementById('editUserPhotoPreview').src = activeAdminUser.photo;
            document.getElementById('editName').value = activeAdminUser.name;
            document.getElementById('editPhone').value = activeAdminUser.phone;
            document.getElementById('editNationalId').value = activeAdminUser.national_id;
            document.getElementById('editPhotoUrl').value = activeAdminUser.photo;
            document.getElementById('editPassword').value = activeAdminUser.pass;
            document.getElementById('pledgeCheck').checked = activeAdminUser.pledge_agreed;
        }

        function saveProfileChanges() {
            const isPledged = document.getElementById('pledgeCheck').checked;
            if(!isPledged) {
                alert("عذراً، يجب الموافقة على التعهد الأمني للمتابعة وحفظ كلمة المرور!");
                return;
            }

            const updatedData = {
                username: activeAdminUser.username,
                name: document.getElementById('editName').value,
                phone: document.getElementById('editPhone').value,
                national_id: document.getElementById('editNationalId').value,
                photo: document.getElementById('editPhotoUrl').value,
                pass: document.getElementById('editPassword').value,
                pledge_agreed: true
            };

            fetch('/api/admin/update_profile', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(updatedData)
            })
            .then(res => res.json())
            .then(data => {
                alert("تم حفظ البيانات وتحديث كلمة المرور والتعهد بنجاح!");
                activeAdminUser = data.user;
                loadProfileData();
            });
        }

        function loadCompaniesTable() {
            fetch('/api/companies')
                .then(res => res.json())
                .then(companies => {
                    const tbody = document.getElementById('companiesTableBody');
                    tbody.innerHTML = '';
                    companies.forEach(c => {
                        const webDisplay = c.website ? `<a href="${c.website}" target="_blank" class="text-wasilCyan underline font-bold">${c.website}</a>` : '<span class="text-gray-400">غير محدد</span>';
                        tbody.innerHTML += `
                            <tr class="border-b hover:bg-gray-50">
                                <td class="p-3 font-bold text-wasilNavy">${c.name}</td>
                                <td class="p-3 font-semibold">${c.contact}</td>
                                <td class="p-3 text-xs">${webDisplay}</td>
                                <td class="p-3 text-center">
                                    <button onclick="deleteCompany(${c.id})" class="bg-red-500 hover:bg-red-600 text-white font-bold text-[10px] px-3 py-1 rounded-lg transition">حذف</button>
                                </td>
                            </tr>
                        `;
                    });
                });
        }

        function addNewCompany(e) {
            e.preventDefault();
            const name = document.getElementById('newCompName').value;
            const contact = document.getElementById('newCompPhone').value;
            const website = document.getElementById('newCompWebsite').value;

            fetch('/api/companies/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name, contact, website })
            })
            .then(res => res.json())
            .then(data => {
                alert("تم إضافة شركة النقل بنجاح!");
                document.getElementById('newCompName').value = '';
                document.getElementById('newCompPhone').value = '';
                document.getElementById('newCompWebsite').value = '';
                loadCompaniesTable();
            });
        }

        function deleteCompany(compId) {
            if(confirm("هل أنت تأكد من حذف هذه الشركة؟")) {
                fetch(`/api/companies/delete/${compId}`, { method: 'DELETE' })
                    .then(res => res.json())
                    .then(data => {
                        alert("تم الحذف بنجاح.");
                        loadCompaniesTable();
                    });
            }
        }

        function loadInternalStaffData() {
            fetch('/api/trips')
                .then(res => res.json())
                .then(trips => {
                    const tbody = document.getElementById('internalStaffTable');
                    tbody.innerHTML = '';
                    trips.forEach(t => {
                        const remaining = t.capacity - t.booked;
                        tbody.innerHTML += `
                            <tr class="border-b">
                                <td class="p-3 font-bold text-wasilNavy">#TRIP-${t.id}</td>
                                <td class="p-3 font-bold">${t.from} - ${t.to}</td>
                                <td class="p-3 font-bold text-wasilOrange">${t.vehicle_type}</td>
                                <td class="p-3 font-bold text-green-600">${remaining} من أصل ${t.capacity}</td>
                                <td class="p-3 text-gray-500 font-mono">${t.tickets.length > 0 ? t.tickets.join(', ') : 'لا يوجد حجوزات'}</td>
                            </tr>
                        `;
                    });
                });
        }

        function loadFullDailySchedule() {
            fetch('/api/trips')
                .then(res => res.json())
                .then(trips => {
                    const container = document.getElementById('fullScheduleContainer');
                    container.innerHTML = '';
                    trips.forEach(t => {
                        container.innerHTML += `
                            <div class="p-3 bg-gray-50 rounded-xl flex justify-between items-center text-xs border border-gray-100">
                                <div>
                                    <span class="font-extrabold text-wasilNavy text-sm block">${t.from} إلى ${t.to}</span>
                                    <span class="text-gray-500">${t.vehicle_type} - مكان الانطلاق: <b>${t.station}</b></span>
                                </div>
                                <div class="text-left">
                                    <span class="bg-wasilCyan/10 text-wasilCyan font-bold px-2 py-0.5 rounded block mb-1">القيام: ${t.time}</span>
                                    <span class="font-black text-wasilOrange">${t.seat_price.toLocaleString()} ج.س</span>
                                </div>
                            </div>
                        `;
                    });
                });
        }

        function loadDriversData() {
            fetch('/api/drivers')
                .then(res => res.json())
                .then(drivers => {
                    const container = document.getElementById('driversListCards');
                    container.innerHTML = '';
                    drivers.forEach(d => {
                        container.innerHTML += `
                            <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 flex items-center gap-3">
                                <img src="${d.photo}" class="w-14 h-14 rounded-full object-cover border-2 border-wasilOrange">
                                <div>
                                    <h4 class="font-extrabold text-wasilNavy text-sm">${d.name}</h4>
                                    <p class="text-xs text-wasilOrange font-semibold">${d.vehicle_model} (${d.vehicle_color})</p>
                                    <span class="text-[10px] text-gray-400">اللوحة: ${d.plate_no} | الهوية: ${d.national_id}</span>
                                </div>
                            </div>
                        `;
                    });
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, announcement=DB["announcement"])

@app.route('/api/trips')
def get_trips():
    return jsonify(DB["trips"])

@app.route('/api/drivers')
def get_drivers():
    return jsonify(DB["drivers"])

@app.route('/api/companies')
def get_companies():
    return jsonify(DB["companies"])

@app.route('/api/announcement/update', methods=['POST'])
def update_announcement():
    data = request.json
    DB["announcement"] = data.get('text', DB["announcement"])
    return jsonify({"status": "success", "announcement": DB["announcement"]})

@app.route('/api/companies/add', methods=['POST'])
def add_company():
    data = request.json
    new_id = len(DB["companies"]) + 1
    new_comp = {
        "id": new_id,
        "name": data.get("name"),
        "contact": data.get("contact"),
        "website": data.get("website", "")
    }
    DB["companies"].append(new_comp)
    return jsonify({"status": "success", "company": new_comp})

@app.route('/api/companies/delete/<int:comp_id>', methods=['DELETE'])
def delete_company(comp_id):
    DB["companies"] = [c for c in DB["companies"] if c["id"] != comp_id]
    return jsonify({"status": "success"})

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    user_key = data.get('userKey')
    password = data.get('pass')
    
    user = DB["admin_users"].get(user_key)
    if user and user["pass"] == password:
        return jsonify({"status": "success", "user": user})
    return jsonify({"status": "error", "message": "كلمة المرور غير صحيحة!"})

@app.route('/api/admin/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    username = data.get('username')
    
    if username in DB["admin_users"]:
        u = DB["admin_users"][username]
        u["name"] = data.get('name')
        u["phone"] = data.get('phone')
        u["national_id"] = data.get('national_id')
        u["photo"] = data.get('photo')
        u["pass"] = data.get('pass')
        u["pledge_agreed"] = data.get('pledge_agreed', True)
        return jsonify({"status": "success", "user": u})
    return jsonify({"status": "error"})

@app.route('/api/book', methods=['POST'])
def book_ticket():
    data = request.json
    trip_id = data.get('tripId')
    ticket_no = f"WSL-{random.randint(1000, 9999)}"
    for trip in DB["trips"]:
        if trip["id"] == trip_id:
            trip["booked"] += 1
            trip["tickets"].append(ticket_no)
            break
    return jsonify({"status": "success", "ticketNo": ticket_no})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/wasil')
def wasil_page():
    return "<h1>سيرفر واصل شغّال على المنفذ 8080 بنجاح 🚀🔥</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

