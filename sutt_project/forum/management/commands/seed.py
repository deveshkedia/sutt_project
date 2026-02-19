from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forum.models import Category, Tags, Thread, Replies, Likes, Report
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data. Use --clear to clear existing data first.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting database seeding...'))

        # Clear existing data if flag is set
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Likes.objects.all().delete()
            Report.objects.all().delete()
            Replies.objects.all().delete()
            Thread.objects.all().delete()
            Tags.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(username__in=[
                'admin', 'john_doe', 'jane_smith', 'alice_wonder', 
                'bob_builder', 'charlie_brown', 'diana_prince', 'evan_rockets'
            ]).delete()
            self.stdout.write(self.style.SUCCESS('✓ Database cleared'))

        # Create Users
        self.stdout.write('Creating users...')
        users = []
        
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        users.append(admin)

        # Create regular users
        user_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'alice_wonder', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Wonder'},
            {'username': 'bob_builder', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Builder'},
            {'username': 'charlie_brown', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
            {'username': 'diana_prince', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Prince'},
            {'username': 'evan_rockets', 'email': 'evan@example.com', 'first_name': 'Evan', 'last_name': 'Rockets'},
        ]

        for user_info in user_data:
            user, created = User.objects.get_or_create(
                username=user_info['username'],
                defaults=user_info
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Create Categories
        self.stdout.write('Creating categories...')
        categories_data = [
            'General Discussion',
            'Announcements',
            'Help & Support',
            'Off-Topic',
            'Feedback',
        ]
        
        categories = []
        for cat_name in categories_data:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            categories.append(cat)

        # Create Tags
        self.stdout.write('Creating tags...')
        tags_data = [
            'python', 'javascript', 'django', 'web-development',
            'database', 'api', 'question', 'tutorial', 'announcement',
            'bug', 'feature', 'help', 'react', 'nodejs', 'frontend', 'backend',
            'performance', 'architecture', 'discussion'
        ]
        
        tags_dict = {}
        for tag_name in tags_data:
            tag, _ = Tags.objects.get_or_create(name=tag_name)
            tags_dict[tag_name] = tag

        # Create 12 Threads
        self.stdout.write('Creating 12 threads...')
        threads_data = [
            {
                'title': 'Getting Started with Django REST Framework',
                'content': '# Django REST Framework Tutorial\n\nI\'ve been learning Django and want to understand REST APIs. Can anyone explain:\n\n- How to set up DRF\n- Creating serializers\n- ViewSets basics\n\nWould appreciate any resources or examples!',
                'author': users[1],
                'category': categories[0],
                'tags': ['django', 'python', 'api', 'tutorial'],
            },
            {
                'title': 'Best practices for database optimization',
                'content': '# Database Performance Questions\n\nI\'m working on a project with large datasets. What are the best practices for:\n\n1. Indexing strategies\n2. Query optimization\n3. Caching mechanisms\n\nAny recommendations would be helpful.',
                'author': users[2],
                'category': categories[0],
                'tags': ['database', 'backend', 'performance'],
            },
            {
                'title': 'System Maintenance Scheduled for Next Week',
                'content': '## Maintenance Notice\n\nPlease be aware that our system will undergo scheduled maintenance on:\n\n**Date:** Next Saturday, 8:00 PM UTC\n**Duration:** 4 hours\n\nDuring this time, the forum will be unavailable. Thank you for your patience!',
                'author': users[0],
                'category': categories[1],
                'tags': ['announcement'],
            },
            {
                'title': 'How to debug JavaScript async/await issues',
                'content': '# Async/Await Debugging Help\n\nI keep running into issues with async/await in my JavaScript code. The promises aren\'t resolving in the expected order.\n\nCan someone help me understand:\n- How async/await works under the hood\n- Common pitfalls\n- Best debugging techniques\n\nI\'ve tried various approaches but still stuck.',
                'author': users[3],
                'category': categories[2],
                'tags': ['javascript', 'help', 'frontend'],
            },
            {
                'title': 'Anyone planning to contribute to open source?',
                'content': '# Open Source Contribution Thread\n\nWho else here is interested in contributing to open source projects? I\'m looking for:\n\n- Good beginner-friendly projects\n- Ways to find issues to work on\n- Tips for making your first PR\n\nLet\'s collaborate and learn together!',
                'author': users[4],
                'category': categories[3],
                'tags': ['help', 'discussion'],
            },
            {
                'title': 'React hooks best practices and patterns',
                'content': '# React Hooks Discussion\n\nAfter working with React hooks for a while, I want to share and discuss best practices:\n\n1. useEffect cleanup patterns\n2. Custom hooks design\n3. Performance optimization with hooks\n4. Testing hooks\n\nWhat are your experiences?',
                'author': users[5],
                'category': categories[0],
                'tags': ['react', 'javascript', 'frontend', 'tutorial'],
            },
            {
                'title': 'Node.js stream handling - best approaches',
                'content': '# Node.js Streams Question\n\nI\'m trying to understand streams in Node.js. How do you handle:\n\n- Readable streams\n- Writable streams\n- Backpressure\n- Error handling in streams\n\nAny code examples would be greatly appreciated!',
                'author': users[1],
                'category': categories[2],
                'tags': ['nodejs', 'backend', 'help'],
            },
            {
                'title': 'Bug: Login page not responsive on mobile',
                'content': '## Bug Report\n\n**Environment:** Latest version\n**Browser:** Chrome Mobile\n\n**Issue:** The login page doesn\'t display correctly on mobile devices. The form elements are cut off.\n\n**Steps to reproduce:**\n1. Open login page on mobile\n2. Try to enter credentials\n3. Observe misalignment\n\n**Expected:** Should be fully responsive',
                'author': users[6],
                'category': categories[2],
                'tags': ['bug', 'frontend'],
            },
            {
                'title': 'Feature Request: Dark mode support',
                'content': '# Feature Request: Dark Mode\n\nMany modern applications have dark mode. It would be great to see this implemented here:\n\n**Benefits:**\n- Reduced eye strain\n- Better for night browsing\n- Currently trending UI feature\n\n**Suggestion:** Could use CSS variables to toggle themes easily.',
                'author': users[2],
                'category': categories[4],
                'tags': ['feature', 'frontend'],
            },
            {
                'title': 'Python FastAPI vs Django - when to use what',
                'content': '# Framework Comparison\n\nI\'m starting a new project and wondering:\n\n- When should I choose FastAPI over Django?\n- Performance comparison\n- Community size and support\n- Learning curve\n- Best use cases for each\n\nWould love to hear from experienced developers!',
                'author': users[3],
                'category': categories[0],
                'tags': ['python', 'api', 'backend', 'question'],
            },
            {
                'title': 'Database schema design for multi-tenant applications',
                'content': '# Multi-Tenant Architecture\n\nDesigning a multi-tenant SaaS platform and need help with database design:\n\n**Options:**\n1. Separate databases per tenant\n2. Shared database with row-level security\n3. Hybrid approach\n\n**Considerations:**\n- Performance\n- Data isolation\n- Scalability\n- Backup complexity\n\nWhat\'s your experience?',
                'author': users[5],
                'category': categories[0],
                'tags': ['database', 'backend', 'architecture'],
            },
            {
                'title': 'Welcome to the Developer Forum!',
                'content': '# Welcome Message\n\nGreat to have you here! This is a place where developers can:\n\n✅ Ask questions\n✅ Share knowledge\n✅ Report bugs\n✅ Request features\n✅ Network with peers\n\nWe encourage respectful and constructive discussions. Happy coding!',
                'author': users[0],
                'category': categories[1],
                'tags': ['announcement'],
            },
        ]

        threads = []
        for thread_data in threads_data:
            tags_list = thread_data.pop('tags')
            thread, created = Thread.objects.get_or_create(
                title=thread_data['title'],
                defaults=thread_data
            )
            if created:
                for tag_name in tags_list:
                    thread.tags.add(tags_dict[tag_name])
            threads.append(thread)

        # Create Replies for threads
        self.stdout.write('Creating replies for threads...')
        
        reply_pool = [
            'Great question! This is a common issue. Let me share what I\'ve learned from my experience.',
            'I had the same problem and found that the documentation covers this pretty well. Check out the official guide.',
            'Have you tried looking at the official examples? They helped me understand this better.',
            'This is a known limitation, but there\'s a workaround that I can share with you.',
            'Thanks for asking! I was wondering about this too. Great thread!',
            'The official docs have a good guide on this topic. I recommend reading it thoroughly.',
            'I can share a code example if you\'d like to see how I solved this problem.',
            'This depends on your specific use case, but generally the best approach is to...',
            'Excellent point! I never thought about it that way before.',
            '+1 for this comment. This is exactly what I was looking for.',
            'Have you considered using library X? It solves this problem elegantly.',
            'I disagree with the previous approach. Here\'s why and here\'s what worked for me instead.',
            'This is still relevant even in 2026. The fundamentals haven\'t changed much.',
            'Great explanation! This clarifies everything for me.',
            'Does anyone else have a different approach to this problem?',
        ]

        # Add 3-5 replies to each thread
        for thread in threads:
            num_replies = random.randint(3, 6)
            for _ in range(num_replies):
                reply_author = random.choice(users[1:])  # Exclude admin
                reply_text = random.choice(reply_pool)
                Replies.objects.get_or_create(
                    thread=thread,
                    content=reply_text,
                    author=reply_author,
                    defaults={'is_deleted': False}
                )

        # Create Likes
        self.stdout.write('Creating likes for threads...')
        for thread in threads:
            num_likes = random.randint(1, 6)
            selected_users = random.sample(users[1:], min(num_likes, len(users) - 1))
            for user in selected_users:
                Likes.objects.get_or_create(thread=thread, user=user)
            thread.likes_count = thread.likes_set.count()
            thread.save()

        # Create Reports for some threads
        self.stdout.write('Creating reports for some threads...')
        report_reasons = ['spam', 'inappropriate', 'harassment', 'misinformation', 'copyright', 'other']
        threads_to_report = random.sample(threads, min(4, len(threads)))
        
        for thread in threads_to_report:
            # Create 1-2 reports per thread
            num_reports = random.randint(1, 2)
            for _ in range(num_reports):
                reporter = random.choice(users[1:])
                reason = random.choice(report_reasons)
                
                # Avoid duplicate reports from same user
                existing = Report.objects.filter(thread=thread, reporter=reporter).exists()
                if not existing:
                    Report.objects.create(
                        thread=thread,
                        reporter=reporter,
                        reason=reason,
                        description=f'This thread contains {reason} content.',
                        status=random.choice(['pending', 'reviewed', 'resolved'])
                    )

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeding completed successfully!'))
        self.stdout.write(self.style.WARNING('\n📊 Seeded data summary:'))
        self.stdout.write(f'  • Users: {User.objects.count()}')
        self.stdout.write(f'  • Categories: {Category.objects.count()}')
        self.stdout.write(f'  • Tags: {Tags.objects.count()}')
        self.stdout.write(f'  • Threads: {Thread.objects.count()}')
        self.stdout.write(f'  • Replies: {Replies.objects.count()}')
        self.stdout.write(f'  • Likes: {Likes.objects.count()}')
        self.stdout.write(f'  • Reports: {Report.objects.count()}')
        self.stdout.write('\n' + self.style.WARNING('🔑 Test login credentials:'))
        self.stdout.write('  • Admin: admin / admin123')
        self.stdout.write('  • User: john_doe / password123')
        self.stdout.write('  • User: jane_smith / password123')
        self.stdout.write('\n' + self.style.WARNING('💡 To clear database before seeding, use:'))
        self.stdout.write('  python manage.py seed --clear')
