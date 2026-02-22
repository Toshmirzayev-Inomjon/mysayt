from django.conf import settings


SUPPORTED_LANGUAGES = {'uz', 'en', 'ru'}
LANGUAGE_SESSION_KEY = 'django_language'


UI_TEXTS = {
    'base.meta_description': {
        'uz': "Django asosida yaratilgan portfolio sayt: loyihalar, texnologiyalar va ishlash jarayoni.",
        'en': "Django-based portfolio website: projects, technologies, and delivery workflow.",
        'ru': "Портфолио на Django: проекты, технологии и процесс разработки.",
    },
    'base.meta_description_og': {
        'uz': "Django asosida yaratilgan portfolio sayt.",
        'en': "Portfolio website built with Django.",
        'ru': "Сайт-портфолио на Django.",
    },
    'nav.projects': {'uz': 'Loyihalar', 'en': 'Projects', 'ru': 'Проекты'},
    'nav.blog': {'uz': 'Blog', 'en': 'Blog', 'ru': 'Блог'},
    'nav.about': {'uz': 'Men haqimda', 'en': 'About', 'ru': 'Обо мне'},
    'nav.contact': {'uz': 'Kontakt', 'en': 'Contact', 'ru': 'Контакты'},
    'nav.booking': {'uz': 'Booking', 'en': 'Booking', 'ru': 'Бронирование'},
    'nav.profile': {'uz': 'Profil', 'en': 'Profile', 'ru': 'Профиль'},
    'nav.logout': {'uz': 'Chiqish', 'en': 'Logout', 'ru': 'Выход'},
    'nav.login': {'uz': 'Kirish', 'en': 'Login', 'ru': 'Вход'},
    'nav.signup': {'uz': "Ro'yxatdan o'tish", 'en': 'Sign up', 'ru': 'Регистрация'},
    'nav.admin': {'uz': 'Admin', 'en': 'Admin', 'ru': 'Админ'},
    'nav.menu': {'uz': 'Menyu', 'en': 'Menu', 'ru': 'Меню'},
    'base.theme_toggle': {
        'uz': 'Mavzuni almashtirish',
        'en': 'Toggle theme',
        'ru': 'Сменить тему',
    },
    'base.footer_powered': {
        'uz': 'Django asosida ishlaydi',
        'en': 'Powered by Django',
        'ru': 'Работает на Django',
    },
    'login.title': {'uz': 'Kirish', 'en': 'Login', 'ru': 'Вход'},
    'login.meta_description': {
        'uz': 'Portfolio akkauntiga kirish sahifasi.',
        'en': 'Sign in page for the portfolio account.',
        'ru': 'Страница входа в аккаунт портфолио.',
    },
    'login.heading': {'uz': 'Tizimga kirish', 'en': 'Sign in', 'ru': 'Войти в систему'},
    'login.submit': {'uz': 'Kirish', 'en': 'Sign in', 'ru': 'Войти'},
    'login.forgot': {
        'uz': 'Parolni unutdingizmi?',
        'en': 'Forgot password?',
        'ru': 'Забыли пароль?',
    },
    'login.no_account': {
        'uz': "Akkaunt yo'qmi?",
        'en': "Don't have an account?",
        'ru': 'Нет аккаунта?',
    },
    'signup.title': {'uz': "Ro'yxatdan o'tish", 'en': 'Sign up', 'ru': 'Регистрация'},
    'signup.meta_description': {
        'uz': "Portfolio uchun yangi akkaunt ro'yxatdan o'tkazish sahifasi.",
        'en': 'Sign up page for creating a new portfolio account.',
        'ru': 'Страница регистрации нового аккаунта портфолио.',
    },
    'signup.heading': {'uz': "Ro'yxatdan o'tish", 'en': 'Create account', 'ru': 'Создать аккаунт'},
    'signup.submit': {'uz': 'Yaratish', 'en': 'Create', 'ru': 'Создать'},
    'signup.notice': {
        'uz': "Ro'yxatdan o'tgach email tasdiqlash havolasi yuboriladi.",
        'en': 'After sign up, an email verification link will be sent.',
        'ru': 'После регистрации будет отправлена ссылка подтверждения email.',
    },
    'signup.have_account': {
        'uz': 'Akkauntingiz bormi?',
        'en': 'Already have an account?',
        'ru': 'Уже есть аккаунт?',
    },
    'pwreset.title': {'uz': 'Parolni tiklash', 'en': 'Reset password', 'ru': 'Сброс пароля'},
    'pwreset.meta_description': {
        'uz': 'Parolni tiklash uchun email yuborish sahifasi.',
        'en': 'Send email page for password reset.',
        'ru': 'Страница отправки email для сброса пароля.',
    },
    'pwreset.heading': {
        'uz': 'Parolni tiklash',
        'en': 'Reset your password',
        'ru': 'Сбросьте пароль',
    },
    'pwreset.description': {
        'uz': 'Email manzilingizni kiriting. Tiklash havolasi yuboriladi.',
        'en': 'Enter your email address. A reset link will be sent.',
        'ru': 'Введите email. Ссылка для сброса будет отправлена.',
    },
    'pwreset.submit': {'uz': 'Havola yuborish', 'en': 'Send link', 'ru': 'Отправить ссылку'},
    'pwreset_done.title': {'uz': 'Email yuborildi', 'en': 'Email sent', 'ru': 'Письмо отправлено'},
    'pwreset_done.heading': {
        'uz': 'Parol tiklash xabari yuborildi',
        'en': 'Password reset message sent',
        'ru': 'Сообщение для сброса отправлено',
    },
    'pwreset_done.description': {
        'uz': "Emailni tekshiring. Havola orqali yangi parol o'rnating.",
        'en': 'Check your email and set a new password using the link.',
        'ru': 'Проверьте email и установите новый пароль по ссылке.',
    },
    'pwreset_confirm.title': {'uz': 'Yangi parol', 'en': 'New password', 'ru': 'Новый пароль'},
    'pwreset_confirm.heading': {
        'uz': 'Yangi parol kiriting',
        'en': 'Enter a new password',
        'ru': 'Введите новый пароль',
    },
    'pwreset_confirm.submit': {'uz': 'Saqlash', 'en': 'Save', 'ru': 'Сохранить'},
    'pwreset_complete.title': {
        'uz': 'Parol yangilandi',
        'en': 'Password updated',
        'ru': 'Пароль обновлен',
    },
    'pwreset_complete.heading': {
        'uz': 'Parol muvaffaqiyatli yangilandi',
        'en': 'Password changed successfully',
        'ru': 'Пароль успешно изменен',
    },
    'pwreset_complete.description': {
        'uz': 'Endi yangi parol bilan tizimga kirishingiz mumkin.',
        'en': 'Now you can sign in with your new password.',
        'ru': 'Теперь можно войти с новым паролем.',
    },
    'home.title': {'uz': 'Portfolio - Asosiy sahifa', 'en': 'Portfolio - Home', 'ru': 'Портфолио - Главная'},
    'home.meta_description': {
        'uz': "Inomjonning portfolio sayti: backend loyihalar, texnologiyalar, tez preview va aloqa formasi.",
        'en': "Inomjon's portfolio: backend projects, technologies, quick previews, and contact form.",
        'ru': 'Портфолио Иномжона: backend-проекты, технологии, быстрый предпросмотр и форма связи.',
    },
    'home.og_description': {
        'uz': "Backend loyihalar va ular qanday ishlashi haqida to'liq ma'lumot.",
        'en': 'Complete details about backend projects and how they work.',
        'ru': 'Подробная информация о backend-проектах и их работе.',
    },
    'home.cta_projects': {
        'uz': "Loyihalarni ko'rish",
        'en': 'View projects',
        'ru': 'Смотреть проекты',
    },
    'home.tag_backend': {'uz': 'Backend Developer', 'en': 'Backend Developer', 'ru': 'Backend-разработчик'},
    'home.cta_contact': {'uz': "Bog'lanish", 'en': 'Contact', 'ru': 'Связаться'},
    'home.cta_cv': {'uz': 'CV yuklab olish', 'en': 'Download CV', 'ru': 'Скачать CV'},
    'home.stats_projects': {'uz': 'Loyihalar', 'en': 'Projects', 'ru': 'Проекты'},
    'home.stats_featured': {'uz': 'Asosiy ishlar', 'en': 'Featured', 'ru': 'Избранное'},
    'home.stats_support': {'uz': "Qo'llab-quvvatlash", 'en': 'Support', 'ru': 'Поддержка'},
    'home.hero_panel_kicker': {'uz': 'Texnik fokus', 'en': 'Tech focus', 'ru': 'Технический фокус'},
    'home.hero_panel_title': {'uz': 'Django ekotizimi', 'en': 'Django ecosystem', 'ru': 'Экосистема Django'},
    'home.hero_focus_point_1': {
        'uz': 'API arxitekturasi va biznes logika',
        'en': 'API architecture and business logic',
        'ru': 'Архитектура API и бизнес-логика',
    },
    'home.hero_focus_point_2': {
        'uz': 'Admin panel va monitoring',
        'en': 'Admin panel and monitoring',
        'ru': 'Админ-панель и мониторинг',
    },
    'home.hero_focus_point_3': {
        'uz': 'Deploy, scale va backup',
        'en': 'Deploy, scale, and backup',
        'ru': 'Деплой, масштабирование и бэкапы',
    },
    'home.about_kicker': {'uz': 'Profil', 'en': 'Profile', 'ru': 'Профиль'},
    'home.about_heading': {'uz': 'Men haqimda', 'en': 'About me', 'ru': 'Обо мне'},
    'home.about_text': {
        'uz': "Arxitektura, toza kod va ishlash tezligiga fokus qilaman. Loyihalarda autentifikatsiya, dashboard, to'lov, admin panel va avtomatlashtirish qismlarini ishlab chiqaman.",
        'en': 'I focus on architecture, clean code, and performance. I build authentication, dashboards, payments, admin panels, and automation.',
        'ru': 'Фокусируюсь на архитектуре, чистом коде и производительности. Разрабатываю аутентификацию, дашборды, платежи, админ-панели и автоматизацию.',
    },
    'home.featured_kicker': {'uz': 'Asosiy', 'en': 'Highlight', 'ru': 'Выборка'},
    'home.featured_heading': {'uz': 'Asosiy loyihalar', 'en': 'Featured projects', 'ru': 'Избранные проекты'},
    'home.featured_chip': {'uz': 'Featured', 'en': 'Featured', 'ru': 'Избранное'},
    'home.project_how_it_works': {
        'uz': "Qanday ishlashini ko'rish",
        'en': 'How it works',
        'ru': 'Как это работает',
    },
    'home.preview': {'uz': 'Tez preview', 'en': 'Quick preview', 'ru': 'Быстрый просмотр'},
    'home.projects_kicker': {'uz': 'Portfolio', 'en': 'Portfolio', 'ru': 'Портфолио'},
    'home.projects_heading': {'uz': 'Barcha loyihalar', 'en': 'All projects', 'ru': 'Все проекты'},
    'home.search_placeholder': {
        'uz': 'Loyiha yoki texnologiya qidiring...',
        'en': 'Search projects or technologies...',
        'ru': 'Поиск проектов или технологий...',
    },
    'home.category_all': {'uz': 'Barcha kategoriyalar', 'en': 'All categories', 'ru': 'Все категории'},
    'home.tag_all': {'uz': 'Barcha taglar', 'en': 'All tags', 'ru': 'Все теги'},
    'home.search_btn': {'uz': 'Qidirish', 'en': 'Search', 'ru': 'Поиск'},
    'home.tech_label': {'uz': 'Texnologiyalar:', 'en': 'Technologies:', 'ru': 'Технологии:'},
    'home.tags_label': {'uz': 'Taglar:', 'en': 'Tags:', 'ru': 'Теги:'},
    'home.result_label': {'uz': 'Natija:', 'en': 'Result:', 'ru': 'Результат:'},
    'home.created_label': {'uz': 'Yaratilgan:', 'en': 'Created:', 'ru': 'Создано:'},
    'home.details_btn': {'uz': 'Batafsil', 'en': 'Details', 'ru': 'Подробнее'},
    'home.demo_video_btn': {'uz': 'Demo video', 'en': 'Demo video', 'ru': 'Демо-видео'},
    'home.no_results': {
        'uz': "Natija topilmadi. So'rovni o'zgartirib ko'ring yoki `/admin/` orqali loyiha qo'shing.",
        'en': 'No results found. Refine your query or add a project via `/admin/`.',
        'ru': 'Ничего не найдено. Уточните запрос или добавьте проект через `/admin/`.',
    },
    'home.services_kicker': {'uz': 'Xizmatlar', 'en': 'Services', 'ru': 'Услуги'},
    'home.services_heading': {'uz': 'Service va pricing', 'en': 'Services and pricing', 'ru': 'Услуги и цены'},
    'home.order_btn': {'uz': 'Buyurtma berish', 'en': 'Order', 'ru': 'Заказать'},
    'home.blog_kicker': {'uz': 'Case study', 'en': 'Case study', 'ru': 'Кейс'},
    'home.blog_heading': {'uz': 'Blog va maqolalar', 'en': 'Blog and articles', 'ru': 'Блог и статьи'},
    'home.read_btn': {'uz': "O'qish", 'en': 'Read', 'ru': 'Читать'},
    'home.all_posts_btn': {'uz': 'Barcha maqolalar', 'en': 'All posts', 'ru': 'Все статьи'},
    'home.no_posts': {'uz': "Blog postlar hali qo'shilmagan.", 'en': 'No blog posts yet.', 'ru': 'Пока нет статей.'},
    'home.testimonials_kicker': {'uz': 'Fikrlar', 'en': 'Testimonials', 'ru': 'Отзывы'},
    'home.testimonials_heading': {'uz': 'Mijozlar fikri', 'en': 'Testimonials', 'ru': 'Отзывы клиентов'},
    'home.contact_kicker': {'uz': 'Aloqa', 'en': 'Contact', 'ru': 'Связь'},
    'home.contact_heading': {'uz': 'Kontakt', 'en': 'Contact', 'ru': 'Контакты'},
    'home.contact_desc': {
        'uz': "Loyiha bo'yicha bog'lanish uchun formani to'ldiring.",
        'en': 'Fill out the form to discuss your project.',
        'ru': 'Заполните форму для обсуждения вашего проекта.',
    },
    'home.contact_submit': {'uz': 'Yuborish', 'en': 'Send', 'ru': 'Отправить'},
    'home.newsletter_kicker': {'uz': 'Newsletter', 'en': 'Newsletter', 'ru': 'Рассылка'},
    'home.newsletter_heading': {
        'uz': "Yangiliklardan xabardor bo'ling",
        'en': 'Stay up to date',
        'ru': 'Будьте в курсе',
    },
    'home.newsletter_submit': {'uz': "Obuna bo'lish", 'en': 'Subscribe', 'ru': 'Подписаться'},
    'home.client_logos_heading': {'uz': 'Mijozlar va hamkorlar', 'en': 'Clients and partners', 'ru': 'Клиенты и партнёры'},
    'home.testimonials_slider_hint': {
        'uz': 'Fikrlar slayderini aylantiring',
        'en': 'Slide through testimonials',
        'ru': 'Листайте отзывы',
    },
    'home.testimonials_prev': {'uz': 'Oldingi', 'en': 'Previous', 'ru': 'Назад'},
    'home.testimonials_next': {'uz': 'Keyingi', 'en': 'Next', 'ru': 'Далее'},
    'home.modal_close': {'uz': 'Yopish', 'en': 'Close', 'ru': 'Закрыть'},
    'home.modal_details_btn': {'uz': "Batafsil ko'rish", 'en': 'View details', 'ru': 'Подробнее'},
    'home.modal_default_title': {'uz': 'Loyiha', 'en': 'Project', 'ru': 'Проект'},
    'blog_list.title': {'uz': 'Blog - Portfolio', 'en': 'Blog - Portfolio', 'ru': 'Блог - Портфолио'},
    'blog_list.meta_description': {
        'uz': "Backend bo'yicha case study va amaliy tajribalar blogi.",
        'en': 'Blog with backend case studies and practical insights.',
        'ru': 'Блог о backend кейсах и практическом опыте.',
    },
    'blog_list.kicker': {'uz': 'Bilimlar', 'en': 'Knowledge', 'ru': 'Знания'},
    'blog_list.heading': {'uz': 'Blog postlar', 'en': 'Blog posts', 'ru': 'Публикации блога'},
    'blog_list.read': {'uz': "O'qish", 'en': 'Read', 'ru': 'Читать'},
    'blog_list.prev': {'uz': 'Oldingi', 'en': 'Previous', 'ru': 'Назад'},
    'blog_list.next': {'uz': 'Keyingi', 'en': 'Next', 'ru': 'Далее'},
    'blog_list.empty': {'uz': "Blog bo'sh.", 'en': 'Blog is empty.', 'ru': 'Блог пуст.'},
    'blog_detail.back': {'uz': '← Blogga qaytish', 'en': '← Back to blog', 'ru': '← Назад к блогу'},
    'profile.title': {'uz': 'Profil', 'en': 'Profile', 'ru': 'Профиль'},
    'profile.meta_description': {
        'uz': 'Foydalanuvchi profil sozlamalari sahifasi.',
        'en': 'User profile settings page.',
        'ru': 'Страница настроек профиля пользователя.',
    },
    'profile.heading': {'uz': 'Profil', 'en': 'Profile', 'ru': 'Профиль'},
    'profile.username': {'uz': 'Username:', 'en': 'Username:', 'ru': 'Имя пользователя:'},
    'profile.email': {'uz': 'Email:', 'en': 'Email:', 'ru': 'Email:'},
    'profile.not_provided': {'uz': 'Kiritilmagan', 'en': 'Not provided', 'ru': 'Не указано'},
    'profile.theme': {'uz': 'Theme:', 'en': 'Theme:', 'ru': 'Тема:'},
    'profile.language': {'uz': 'Til:', 'en': 'Language:', 'ru': 'Язык:'},
    'profile.twofa': {'uz': '2FA:', 'en': '2FA:', 'ru': '2FA:'},
    'profile.enabled': {'uz': 'Yoqilgan', 'en': 'Enabled', 'ru': 'Включено'},
    'profile.disabled': {'uz': 'Yoqilmagan', 'en': 'Disabled', 'ru': 'Выключено'},
    'profile.kicker': {'uz': 'Akkaunt', 'en': 'Account', 'ru': 'Аккаунт'},
    'profile.theme_dark': {'uz': 'Qora', 'en': 'Dark', 'ru': 'Тёмная'},
    'profile.theme_light': {'uz': 'Yorug', 'en': 'Light', 'ru': 'Светлая'},
    'profile.theme_save': {'uz': 'Theme saqlash', 'en': 'Save theme', 'ru': 'Сохранить тему'},
    'profile.home_btn': {'uz': 'Asosiy sahifa', 'en': 'Home', 'ru': 'Главная'},
    'profile.password_update': {'uz': 'Parolni yangilash', 'en': 'Update password', 'ru': 'Обновить пароль'},
    'profile.otp_setup': {'uz': '2FA setup', 'en': '2FA setup', 'ru': 'Настройка 2FA'},
    'profile.otp_verify': {'uz': '2FA verify', 'en': '2FA verify', 'ru': 'Проверка 2FA'},
    'booking.title': {'uz': 'Booking', 'en': 'Booking', 'ru': 'Бронирование'},
    'booking.meta_description': {
        'uz': "Qo'ng'iroq yoki konsultatsiya uchun booking sahifasi.",
        'en': 'Booking page for consultation calls.',
        'ru': 'Страница бронирования консультации/звонка.',
    },
    'booking.heading': {'uz': 'Call booking', 'en': 'Call booking', 'ru': 'Бронирование звонка'},
    'booking.kicker': {'uz': "Qo'ng'iroq", 'en': 'Call', 'ru': 'Звонок'},
    'booking.slot_heading': {'uz': 'Tayyor slotlar', 'en': 'Available slots', 'ru': 'Доступные слоты'},
    'booking.slot_hint': {
        'uz': "Quyidagi slotlardan birini bossangiz, sana avtomatik maydonga tushadi.",
        'en': 'Click any slot below to auto-fill the date field.',
        'ru': 'Нажмите слот ниже, чтобы дата автоматически подставилась в поле.',
    },
    'booking.slot_pick': {'uz': 'Tanlash', 'en': 'Pick', 'ru': 'Выбрать'},
    'booking.quick_contact_heading': {'uz': 'Tez aloqa', 'en': 'Quick contact', 'ru': 'Быстрый контакт'},
    'booking.quick_contact_desc': {
        'uz': "Agar xohlasangiz, darhol Telegram yoki WhatsApp orqali ham yozishingiz mumkin.",
        'en': 'You can also reach out instantly via Telegram or WhatsApp.',
        'ru': 'Вы также можете написать сразу в Telegram или WhatsApp.',
    },
    'booking.quick_contact_whatsapp': {'uz': 'WhatsApp yozish', 'en': 'Message on WhatsApp', 'ru': 'Написать в WhatsApp'},
    'booking.quick_contact_telegram': {'uz': 'Telegram yozish', 'en': 'Message on Telegram', 'ru': 'Написать в Telegram'},
    'booking.quick_contact_missing': {
        'uz': "Tez aloqa havolalari hali sozlanmagan.",
        'en': 'Quick contact links are not configured yet.',
        'ru': 'Ссылки для быстрого контакта пока не настроены.',
    },
    'booking.submit': {'uz': "So'rov yuborish", 'en': 'Send request', 'ru': 'Отправить запрос'},
    'project.back_home': {'uz': '← Asosiyga qaytish', 'en': '← Back to home', 'ru': '← Назад на главную'},
    'project.created_date': {'uz': 'Yaratilgan sana:', 'en': 'Created at:', 'ru': 'Дата создания:'},
    'project.description': {'uz': 'Tavsif', 'en': 'Description', 'ru': 'Описание'},
    'project.results': {'uz': 'Natijalar', 'en': 'Results', 'ru': 'Результаты'},
    'project.technologies': {'uz': 'Texnologiyalar', 'en': 'Technologies', 'ru': 'Технологии'},
    'project.live_demo': {'uz': 'Live Demo', 'en': 'Live Demo', 'ru': 'Демо'},
    'project.demo_video': {'uz': 'Demo Video', 'en': 'Demo Video', 'ru': 'Демо-видео'},
    'project.demo_video_heading': {'uz': 'Demo video', 'en': 'Demo video', 'ru': 'Демо-видео'},
    'project.video_link': {'uz': 'Video havola:', 'en': 'Video link:', 'ru': 'Ссылка на видео:'},
    'project.case_study_chip': {'uz': 'Case study', 'en': 'Case study', 'ru': 'Кейс'},
    'project.metrics_heading': {'uz': 'Before / After natijalar', 'en': 'Before / After results', 'ru': 'Результаты до / после'},
    'project.metric_before': {'uz': 'Oldingi holat', 'en': 'Before', 'ru': 'До'},
    'project.metric_after': {'uz': 'Yangi holat', 'en': 'After', 'ru': 'После'},
    'project.how_it_works': {'uz': 'Qanday ishlaydi', 'en': 'How it works', 'ru': 'Как работает'},
    'project.screenshots': {'uz': 'Screenshotlar', 'en': 'Screenshots', 'ru': 'Скриншоты'},
    'otp_setup.title': {'uz': '2FA Setup', 'en': '2FA Setup', 'ru': 'Настройка 2FA'},
    'otp_setup.heading': {'uz': '2FA setup', 'en': '2FA setup', 'ru': 'Настройка 2FA'},
    'otp_setup.description': {
        'uz': "Authenticator app orqali quyidagi URL ni qo'shing:",
        'en': 'Add the following URL in your authenticator app:',
        'ru': 'Добавьте следующий URL в приложение-аутентификатор:',
    },
    'otp_setup.verify_btn': {
        'uz': 'OTP kodni tasdiqlash',
        'en': 'Verify OTP code',
        'ru': 'Подтвердить OTP-код',
    },
    'otp_verify.title': {'uz': '2FA Verify', 'en': '2FA Verify', 'ru': 'Проверка 2FA'},
    'otp_verify.heading': {'uz': 'OTP tasdiqlash', 'en': 'Verify OTP', 'ru': 'Подтверждение OTP'},
    'otp_verify.submit': {'uz': 'Tasdiqlash', 'en': 'Verify', 'ru': 'Подтвердить'},
    'auth.kicker_account': {'uz': 'Akkaunt', 'en': 'Account', 'ru': 'Аккаунт'},
    'auth.kicker_security': {'uz': 'Xavfsizlik', 'en': 'Security', 'ru': 'Безопасность'},
    'msg.smtp_fallback': {
        'uz': 'SMTP ishlamadi. Vaqtinchalik reset link: {link}',
        'en': 'SMTP is unavailable. Temporary reset link: {link}',
        'ru': 'SMTP недоступен. Временная ссылка для сброса: {link}',
    },
    'msg.smtp_error': {
        'uz': "Email yuborishda xatolik. SMTP sozlamalarini yoki internet ulanishini tekshirib qayta urinib ko'ring.",
        'en': 'Failed to send email. Check SMTP settings or internet connection and try again.',
        'ru': 'Не удалось отправить email. Проверьте SMTP-настройки или интернет и попробуйте снова.',
    },
    'msg.contact_throttle': {
        'uz': "Juda ko'p xabar yuborildi. Iltimos, {wait_minutes} daqiqadan keyin qayta urinib ko'ring.",
        'en': 'Too many messages sent. Please try again in {wait_minutes} minutes.',
        'ru': 'Слишком много сообщений. Попробуйте снова через {wait_minutes} минут.',
    },
    'msg.contact_sent': {
        'uz': 'Xabaringiz yuborildi. Tez orada javob beraman.',
        'en': 'Your message has been sent. I will get back to you soon.',
        'ru': 'Ваше сообщение отправлено. Я скоро отвечу.',
    },
    'msg.recaptcha_failed': {
        'uz': "reCAPTCHA tasdiqlanmadi. Iltimos, qayta urinib ko'ring.",
        'en': 'reCAPTCHA verification failed. Please try again.',
        'ru': 'Проверка reCAPTCHA не пройдена. Попробуйте снова.',
    },
    'msg.login_rate_limited': {
        'uz': "Kirish urinishlari cheklangan. Iltimos, {wait_minutes} daqiqadan keyin urinib ko'ring.",
        'en': 'Login attempts are temporarily limited. Please try again in {wait_minutes} minutes.',
        'ru': 'Попытки входа временно ограничены. Повторите через {wait_minutes} минут.',
    },
    'msg.password_reset_rate_limited': {
        'uz': "Parol tiklash urinishlari ko'payib ketdi. Iltimos, {wait_minutes} daqiqadan keyin qayta urinib ko'ring.",
        'en': 'Too many password reset attempts. Please try again in {wait_minutes} minutes.',
        'ru': 'Слишком много попыток сброса пароля. Попробуйте снова через {wait_minutes} минут.',
    },
    'msg.signup_active': {
        'uz': "Ro'yxatdan o'tish yakunlandi. Hisobingiz darhol faollashtirildi.",
        'en': 'Sign up completed. Your account was activated immediately.',
        'ru': 'Регистрация завершена. Ваш аккаунт активирован сразу.',
    },
    'msg.signup_verify': {
        'uz': "Ro'yxatdan o'tish yakunlandi. Emailingizni tasdiqlang.",
        'en': 'Sign up completed. Please verify your email.',
        'ru': 'Регистрация завершена. Подтвердите email.',
    },
    'msg.verify_invalid': {
        'uz': "Tasdiqlash tokeni noto'g'ri yoki muddati o'tgan.",
        'en': 'Verification token is invalid or expired.',
        'ru': 'Токен подтверждения неверный или просрочен.',
    },
    'msg.verify_success': {
        'uz': 'Email tasdiqlandi. Endi tizimga kirishingiz mumkin.',
        'en': 'Email verified. You can now sign in.',
        'ru': 'Email подтвержден. Теперь можно войти.',
    },
    'msg.newsletter_success': {
        'uz': "Newsletter obuna muvaffaqiyatli qo'shildi.",
        'en': 'Newsletter subscription completed.',
        'ru': 'Подписка на рассылку оформлена.',
    },
    'msg.newsletter_error': {
        'uz': "Newsletter email noto'g'ri.",
        'en': 'Invalid newsletter email.',
        'ru': 'Некорректный email для рассылки.',
    },
    'msg.booking_success': {
        'uz': "Call booking so'rovi qabul qilindi.",
        'en': 'Call booking request received.',
        'ru': 'Запрос на звонок принят.',
    },
    'msg.otp_package_missing': {
        'uz': "2FA paketi o'rnatilmagan.",
        'en': '2FA package is not installed.',
        'ru': 'Пакет 2FA не установлен.',
    },
    'msg.otp_setup_first': {
        'uz': 'Avval 2FA setup qiling.',
        'en': 'Set up 2FA first.',
        'ru': 'Сначала настройте 2FA.',
    },
    'msg.otp_enabled': {
        'uz': '2FA muvaffaqiyatli yoqildi.',
        'en': '2FA enabled successfully.',
        'ru': '2FA успешно включена.',
    },
    'msg.otp_invalid': {
        'uz': "OTP kod noto'g'ri.",
        'en': 'Invalid OTP code.',
        'ru': 'Неверный OTP-код.',
    },
}


def normalize_language(code):
    if not code:
        return 'uz'
    base = str(code).replace('_', '-').split('-')[0].lower()
    if base in SUPPORTED_LANGUAGES:
        return base
    return 'uz'


def get_language(request=None, language=''):
    if language:
        return normalize_language(language)
    if request is not None:
        session_lang = ''
        if hasattr(request, 'session'):
            session_lang = request.session.get(settings.LANGUAGE_COOKIE_NAME, '') or request.session.get(
                LANGUAGE_SESSION_KEY, ''
            )
        request_lang = getattr(request, 'LANGUAGE_CODE', '')
        return normalize_language(session_lang or request_lang)
    return 'uz'


def t(key, request=None, language='', **kwargs):
    lang = get_language(request=request, language=language)
    entry = UI_TEXTS.get(key, {})
    text = entry.get(lang) or entry.get('uz') or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
