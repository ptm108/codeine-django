from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone

from common.models import BaseUser, Member, Partner, Organization, BankDetail, MembershipSubscription, PaymentTransaction
from courses.models import (
    Course,
    Chapter,
    CourseMaterial,
    CourseFile,
    Video,
    CourseReview,
    Quiz,
    QuizResult,
    Question,
    ShortAnswer,
    MCQ,
    MRQ,
    CourseComment,
    QuestionBank,
    QuestionGroup,
    Enrollment
)
from community.models import CodeReview, CodeReviewComment, Article
from consultations.models import ConsultationSlot, ConsultationApplication
from analytics.models import EventLog
from industry_projects.models import IndustryProject, IndustryProjectApplication
from helpdesk.models import Ticket, TicketMessage
from achievements.models import Achievement, AchievementRequirement

import sys
from datetime import timedelta, datetime
from random import randint, seed
from hashids import Hashids


class Command(BaseCommand):
    help = 'Prepopulates the database with data for demo'

    def handle(self, *args, **options):
        # raise CommandError('Error')
        # self.stdout.write('Hello' + self.style.SUCCESS('Success'))

        # global refs
        admin = None
        hashids = Hashids(min_length=5)
        seed(42)

        # instantiate admins
        self.stdout.write('Creating superuser...')
        try:
            u = BaseUser.objects.create_superuser(
                'a@a.com',
                'password',
                first_name='David',
                last_name='Chen',
            )
            u.save()

            admin = u
            self.stdout.write(f'{self.style.SUCCESS("Success")}: Superuser instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # instantiate members
        self.stdout.write('Creating members...')
        try:
            locations = ['Singapore', 'London, United Kingdom', 'Texas, USA', 'Surabaya, Indonesia']
            genders = ['M', 'F', 'U']

            u = BaseUser.objects.create_user(
                'm1@m1.com',
                'password',
                first_name='Jonathan',
                last_name='Chan',
                is_active=True,
                gender='M',
                location='Singapore',
            )
            u.profile_photo.save('m1.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/m1.jpeg', 'rb')))
            u.save()

            m = Member(
                user=u, 
                unique_id=hashids.encode(int(u.id))[:5], 
                membership_tier='PRO', 
                stats={
                    'PY': randint(70, 300),
                    'JAVA': randint(70, 300),
                    'JS': randint(80, 800),
                    'CPP': randint(100, 300),
                    'CS': randint(90, 300),
                    'HTML': randint(70, 600),
                    'CSS': randint(120, 800),
                    'RUBY': randint(130, 200),
                    'SEC': randint(20, 100),
                    'DB': randint(50, 300),
                    'FE': randint(80, 500),
                    'BE': randint(150, 300),
                    'UI': randint(200, 300),
                    'ML': randint(10, 300),
                }
            )
            m.save()

            pt = PaymentTransaction(
                payment_amount=5.99,
                payment_type='AMEX',
                payment_status='COMPLETED',
            )
            pt.save()

            now = timezone.now()
            MembershipSubscription(
                payment_transaction=pt,
                expiry_date=timezone.make_aware(datetime(now.year, now.month + 1, 1)),
                member=m
            ).save()

            u = BaseUser.objects.create_user(
                'm2@m2.com',
                'password',
                first_name='Suzuki',
                last_name='Haneda',
                is_active=True,
                gender='M',
                location='Haneda, Japan',
            )
            u.profile_photo.save('m2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/m2.jpeg', 'rb')))
            u.save()

            m = Member(user=u, unique_id=hashids.encode(int(u.id))[:5])
            m.save()

            for i in range(3, 31):
                u = BaseUser.objects.create_user(
                    f'm{i}@m{i}.com',
                    'password',
                    first_name='Member',
                    last_name=str(i),
                    is_active=True,
                    gender=genders[randint(0, 2)],
                    location=locations[randint(0, 3)]
                )
                u.save()

                m = Member(
                    user=u,
                    unique_id=hashids.encode(int(u.id))[:5],
                    stats={
                        'PY': randint(100, 1500),
                        'JAVA': randint(100, 1800),
                        'JS': randint(100, 1500),
                        'CPP': randint(100, 1600),
                        'CS': randint(100, 1700),
                        'HTML': randint(100, 1800),
                        'CSS': randint(100, 1500),
                        'RUBY': randint(100, 1400),
                        'SEC': randint(100, 1700),
                        'DB': randint(100, 1800),
                        'FE': randint(100, 1900),
                        'BE': randint(100, 1400),
                        'UI': randint(100, 1300),
                        'ML': randint(100, 1200),
                    },
                )
                m.save()
                pt = PaymentTransaction(
                    payment_amount=5.99,
                    payment_type='AMEX',
                    payment_status='COMPLETED',
                )
                pt.save()

                now = timezone.now()
                MembershipSubscription(
                    payment_transaction=pt,
                    expiry_date=timezone.make_aware(datetime(now.year, now.month + 1, 1)),
                    member=m
                ).save()
            # end for

            self.stdout.write(f'{self.style.SUCCESS("Success")}: {Member.objects.count()} members instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # instantiate partners
        self.stdout.write('Creating partners...')
        try:
            u = BaseUser.objects.create_user(
                'p1@p1.com',
                'password',
                first_name='Shaun',
                last_name='Pelling',
                is_active=True
            )
            u.profile_photo.save('p1.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/p1.jpeg', 'rb')))
            u.save()

            p = Partner(user=u, job_title='Net Ninja', bio='I ninja through the net')
            p.save()

            bd = BankDetail(
                bank_account='1234567890',
                bank_name='DBS',
                swift_code='123',
                bank_country='Singapore',
                bank_address='1 Tras St Singapore 123456',
                partner=p
            )
            bd.save()

            u = BaseUser.objects.create_user(
                'p2@p2.com',
                'password',
                first_name='Suzuki',
                last_name='Haneda',
                is_active=True
            )
            u.profile_photo.save('p2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/p2.jpeg', 'rb')))
            u.save()

            p = Partner(user=u, job_title='Ohayogo', bio='Watashi wa suzuki dessssss')
            p.save()

            bd = BankDetail(
                bank_account='1234567890',
                bank_name='DBS',
                swift_code='123',
                bank_country='Singapore',
                bank_address='1 Tras St Singapore 123456',
                partner=p
            )
            bd.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: {Partner.objects.count()} partners instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # instantiate enterprise partners
        self.stdout.write('Creating enterprise partners...')
        try:
            o = Organization(organization_name='Apple')
            o.organization_photo.save('apple.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/apple.jpeg', 'rb')))
            o.save()

            u = BaseUser.objects.create_user(
                'ep1@ep1.com',
                'password',
                first_name='Steve',
                last_name='Jobs',
                is_active=True
            )
            u.profile_photo.save('ep1.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/ep1.jpeg', 'rb')))
            u.save()

            p = Partner(user=u, job_title='CEO', bio='I create jobs', org_admin=True, organization=o)
            p.save()

            bd = BankDetail(
                bank_account='1234567890',
                bank_name='DBS',
                swift_code='123',
                bank_country='Singapore',
                bank_address='1 Tras St Singapore 123456',
                partner=p
            )
            bd.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: 1 x Steve Jobs (Enterprise: Apple) instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            o = Organization(organization_name='Stanford University')
            o.organization_photo.save('stanford.png', ImageFile(open('./codeine_django/common/management/demo_assets/stanford.png', 'rb')))
            o.save()

            u = BaseUser.objects.create_user(
                'ep2@ep2.com',
                'password',
                first_name='Andrew',
                last_name='Ng',
                is_active=True
            )
            u.profile_photo.save('ep2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/ep2.jpg', 'rb')))
            u.save()

            p = Partner(user=u, job_title='Lecturer', bio='ML is my passion', org_admin=True, organization=o)
            p.save()

            bd = BankDetail(
                bank_account='1234567890',
                bank_name='DBS',
                swift_code='123',
                bank_country='Singapore',
                bank_address='1 Tras St Singapore 123456',
                partner=p
            )
            bd.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: 1 x Andrew Ng (Enterprise: Stanford U) instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # creating a React Course
        self.stdout.write('Creating courses...')
        try:
            partner = Partner.objects.get(user__first_name='Andrew')
            members = Member.objects.exclude(user__email='m1@m1.com').exclude(user__email='m2@m2.com').all()

            c = Course(
                title='React Native for Beginners',
                learning_objectives=['React Native Novice to Ninja!', 'Create a React Native app from Scratch'],
                requirements=['Node Package Manager', 'Basic Javascript Knowledge'],
                description='Hey gang, and welcome to your first React Native tutorial for beginners. In this series we\'ll go from novice to ninja and create a React Native app from scratch. First though, we\'ll get set up and talk about what React Native actually is.',
                introduction_video_url='https://www.youtube.com/watch?v=ur6I5m2nTvk',
                github_repo='https://github.com/ptm108/Graspfood2.git',
                coding_languages=['JS', 'HTML', 'CSS'],
                languages=['ENG'],
                categories=['FE', 'UI'],
                is_published=True,
                published_date=timezone.now(),
                pro=False,
                duration=9,
                exp_points=230,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course1/courseimage.png', 'rb')))
            c.save()

            # create some fake enrollments
            for m in members:
                Enrollment(
                    progress=0,
                    course=c,
                    member=m,
                ).save()
            # end for

            # create some fake views
            for u in BaseUser.objects.all():
                EventLog(
                    payload='course view',
                    user=u,
                    course=c
                ).save()
            # end for

            # chapters
            chap = Chapter(
                title='React Native App Basics',
                overview='Hey gang, in this React Native tutorial we\'ll talk about the different way to create a React Native app, and use Expo to create ours. I\'ll also show you how to run the app on a real device & android emulator. \n\n f you download the repo code / clone the repo, you will need to run npm install in the project directory to install any project dependencies first. Without doing this, the code may not work as expected.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Github repo',
                description='This repo contains all the course files for the React Tutorial for Beginners playlist on The Net Ninja Playlist, Each lesson in the series has its own branch, so you\'ll need to select that branch to see the code for that lesson. E.g. to see the code for lesson 10, you would select the lesson-10 branch.',
                material_type='FILE',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cf = CourseFile(
                course_material=cm,
                google_drive_url='https://github.com/iamshaunjp/react-native-tutorial',
            )
            cf.zip_file.save('react-native-tutorial-master.zip', File(open('./codeine_django/common/management/demo_assets/course1/react-native-tutorial-master.zip', 'rb')))
            cf.save()

            cm = CourseMaterial(
                title='React Native Tutorial #2 - Creating a React Native App',
                description='Hey gang, in this React Native tutorial we\'ll talk about the different way to create a React Native app, and use Expo to create ours. I\'ll also show you how to run the app on a real device & android emulator. \n\n f you download the repo code / clone the repo, you will need to run npm install in the project directory to install any project dependencies first. Without doing this, the code may not work as expected.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://www.youtube.com/watch?v=pflXnUNMsNk'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #3 - Views, Text & Styles',
                description='In this React Native tutorial for beginners we\'ll take a look at 2 built-in components - the View component and the Text component. We\'ll also see how to create a "stylesheet" in React Native too, to style our components.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://www.youtube.com/watch?v=_YydVvnjNFE'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #4 - Using State',
                description='In this React Native tutorial I\'ll show you how we can use state in our components. This is very similar to how we would use state in a standard React web app.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/1FiIYaRr148'
            )
            cv.save()

            cm = CourseMaterial(
                title='Quiz 1',
                description='Hey gang, let\'s test your knowledge',
                material_type='QUIZ',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            qb = QuestionBank(
                label='Easy',
                course=c,
            )
            qb.save()

            qn = Question(
                title='How do you start your local development server?',
                subtitle='Hint: it\'s the same with ReactJS',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['npm start', 'npm run start', 'npm install', 'npm run dev'],
                correct_answer='npm start'
            )
            mcq.save()

            qn = Question(
                title='How do you install npm packages?',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['npm install <package>', 'npm i <package>', 'npm run <package>', 'npm <package>'],
                correct_answer=['npm install <package>', 'npm i <package>']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is your mother?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            q = Quiz(
                course_material=cm,
                passing_marks=0,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            chap = Chapter(
                title='React Native App Forms',
                overview='Text Inputs, List/Scroll Views, Touchable Components',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='React Native Tutorial #5 - Text Inputs',
                description='Hey gang, in this React Native tutorial we\'ll take a look at capturing user input by using Text Input components. These come baked into the React Native library.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/c9Sg9jDitm8'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #6 - Lists & ScrollView',
                description='In this React Native tutorial for beginners we\'ll talk about how to display lists of data in our apps. To do this we also need to look at a component called ScrollView, which allows us to scroll through long lists that are bigger than the area available on the screen',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/W-pg1r6-T0g'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #7 - Flat List Component',
                description='In this React Native tutorial I\'ll take a look at another way to output lists of data - using the FlatList component',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/iMCM1NceGJY'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #8 - Touchable Components',
                description='In this React Native tutorial we\'ll see how to create touchable components, and wrap them around other components so that they can be pressed (much like a button component)',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/QhX25YGf8qg'
            )
            cv.save()

            chap = Chapter(
                title='The Todo App',
                overview='We\'re gonna create a todo app now.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='React Native Tutorial #9 - Todo App (part 1)',
                description='In this React Native tutorial we\'ll start our first project - a simple todo app - which will bring together everything we\'ve learnt so far, plus a few other things too.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/uLHFPt9B2Os'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #10 - Todo App (part 2)',
                description='In this React Native tutorial we\'ll carry on with the todo list app we started in the last lesson.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/SGEitne8N-Q'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #11 - Todo App (part 3)',
                description='In this React Native tutorial we\'ll finish up the Todo app by adding a form to add new todos to the list.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/LH_SoXiu_Hk'
            )
            cv.save()

            chap = Chapter(
                title='Accessing Native Mobile Functions',
                overview='Alerts, Dismiss Keyboard',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='React Native Tutorial #12 - Alerts',
                description='In this React Native tutorial we\'ll take a look at alert boxes and how to use them in our app.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/oVA9JgTTiT0'
            )
            cv.save()

            cm = CourseMaterial(
                title='React Native Tutorial #13 - Dismissing the Keyboard',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/oVA9JgTTiT0'
            )
            cv.save()

            chap = Chapter(
                title='FlexBoxes',
                overview='Flex them boxes',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='React Native Tutorial #14 - Flexbox Basics',
                description='In this React Native tutorial we\'ll take a look at Flexbox, which can be used to layout the different components in our app.',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/R2eqAgR_KlU'
            )
            cv.save()

            qb = QuestionBank(
                label='Easy - Final Assessment',
                course=c,
            )
            qb.save()

            qn = Question(
                title='How do you start your local development server?',
                subtitle='Hint: it\'s the same with ReactJS',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['npm start', 'npm run start', 'npm install', 'npm run dev'],
                correct_answer='npm start'
            )
            mcq.save()

            qn = Question(
                title='How do you install npm packages?',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['npm install <package>', 'npm i <package>', 'npm run <package>', 'npm <package>'],
                correct_answer=['npm install <package>', 'npm i <package>']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard - Final Assessment',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is your mother?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            # create some fake enrollments
            for m in members:
                QuizResult(
                    quiz=q,
                    member=m,
                    passed=False if randint(0, 2) > 0 else True,
                    submitted=True,
                    score=randint(0, 5)
                ).save()
            # end for

            self.stdout.write(f'{self.style.SUCCESS("Success")}: React Native Course created')
        except:
            e = sys.exc_info()[0]
            print(e + '')
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {e}')
        # end try-except

        try:
            partner = Partner.objects.get(user__first_name='Andrew')

            c = Course(
                title='Stanford CS229: Machine Learning (Autumn 2018)',
                learning_objectives=['Supervised Learning (Linear and Logistic Regression, General Linearized Models (GLMs), Gaussian Discriminant Analysis (GDA), Generative/Discriminative Learning, Neural Networks, Support Vector Machines (SVM))', 'Unsupervised Learning (Expectation-Maximization (K-Means, etc.), Principal Component Analysis (PCA), Dimensionality Reduction)'],
                requirements=['Proficiency in Python', 'College Calculus, Linear Algebra', 'Basic Probability and Statistics'],
                description='In this era of big data, there is an increasing need to develop and deploy algorithms that can analyze and identify connections in that data. Using machine learning (a subset of artificial intelligence) it is now possible to create computer systems that automatically improve with experience. This technology has numerous real-world applications including robotic control, data mining, autonomous navigation, and bioinformatics. This course features classroom videos and assignments adapted from the CS229 graduate course as delivered on-campus at Stanford in Autumn 2018 and Autumn 2019. In order to make the content and workload more manageable for working professionals, the course has been split into two parts, XCS229i: Machine Learning and XCS229ii: Machine Learning Strategy and Intro to Reinforcement Learning.',
                introduction_video_url='https://youtu.be/jGwO_UgTS7I',
                coding_languages=['PY'],
                languages=['ENG'],
                categories=['ML'],
                is_published=True,
                published_date=timezone.now(),
                pro=False,
                duration=9,
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course2/course2.jpg', 'rb')))
            c.save()

            # create some fake views
            for u in BaseUser.objects.all():
                EventLog(
                    payload='course view',
                    user=u,
                    course=c
                ).save()
            # end for

            # chapters
            chap = Chapter(
                title='Lecture 1',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Welcome | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/jGwO_UgTS7I'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 2',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Linear Regression and Gradient Descent | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/4b4MUYve_U8'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 3',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Locally Weighted & Logistic Regression | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/het9HFqo1TQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 4',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Perceptron & Generalized Linear Model | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/iZTeva0WSTQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 5',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='GDA & Naive Bayes | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/nt63k3bfXS0'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 6',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Lecture 6 - Support Vector Machines | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/lDwow4aOrtg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 7',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Kernels | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/8NYoQiRANpg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 8',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title=' Data Splits, Models & Cross-Validation | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/rjbkWSTjHzM'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 9',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Approx/Estimation Error & ERM | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/iVOxMcumR4A'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 10',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Decision Trees and Ensemble Methods | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/wr9gUr-eWdA'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 11',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Introduction to Neural Networks | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/MfIjxPh6Pys'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 12',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Backprop & Improving Neural Networks | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/zUazLXZZA2U'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 13',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Debugging ML Models and Error Analysis | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/ORrStCArmP4'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 14',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Expectation-Maximization Algorithms | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/rVfZHWTwXSA'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 15',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='EM Algorithm & Factor Analysis | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/tw6cmL5STuY'
            )
            cv.save()

            qb = QuestionBank(
                label='Easy',
                course=c,
            )
            qb.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['SSSP', 'Aho-Corasick', 'Random Tree Classifier'],
                correct_answer='Random Tree Classifier'
            )
            mcq.save()

            qn = Question(
                title='Risheng is...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Machine Learning Course created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            partner = Partner.objects.all()[1]

            c = Course(
                title='Django Framework (3.0) Crash Course Tutorials',
                learning_objectives=['Create a customer relationship management tool with Django', 'Learning Basic Database Relationships', 'Build a backend with python'],
                requirements=['Basic Python Knowledge', 'Experience with REST'],
                description='Get started with Django!',
                introduction_video_url='https://youtu.be/xv_bwpA_aEA',
                coding_languages=['PY'],
                languages=['ENG'],
                categories=['BE', 'DB'],
                is_published=True,
                published_date=timezone.now(),
                pro=True,
                duration=9,
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course3/course3.png', 'rb')))
            c.save()

            # create some fake views
            for u in BaseUser.objects.all():
                EventLog(
                    payload='course view',
                    user=u,
                    course=c
                ).save()
            # end for

            # chapters
            chap = Chapter(
                title='What is Django?',
                overview='In these tutorials we will will be building a customer management app. Part one will cover installing django and getting our basic app setup.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Github repo',
                description='This repo contains all the course files.',
                material_type='FILE',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cf = CourseFile(
                course_material=cm,
                google_drive_url='https://github.com/divanov11/crash-course-CRM/tree/Part-1-Installation-%26-App',
            )
            cf.save()

            cm = CourseMaterial(
                title='What is Django? | Getting Started',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/xv_bwpA_aEA'
            )
            cv.save()

            chap = Chapter(
                title='URLS and Views',
                overview='Django URL routing and views introduction. Part 2 of my django crash course serries.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='URLS and Views',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/4b4MUYve_U8'
            )
            cv.save()

            chap = Chapter(
                title='Templates & Inheritance',
                overview='Introduction to django templates and template inheriting. Part 3 of my django crash course serries.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Templates & Inheritance',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/9aEsZxaOwRs'
            )
            cv.save()

            chap = Chapter(
                title='Static Files & Images',
                overview='Introduction to django static files. Part 4 of my django crash course serries.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Static Files & Images',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/kqyfEz7TNI0'
            )
            cv.save()

            chap = Chapter(
                title='Database Models & Admin Panel',
                overview='Introduction to django admin panel and models. Part 5 of my django crash course serries.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Database Models & Admin Panel',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/mOu9fpfzyUg'
            )
            cv.save()

            chap = Chapter(
                title='Database Relationships',
                overview='ntroduction to Database model relationships. In this video we will be covering "One to Many" and "Many to Many" relationships and how this is implemented in Django.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='One To Many & Many to Many',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/wIPHER2UBB4'
            )
            cv.save()

            qb = QuestionBank(
                label='Easy',
                course=c,
            )
            qb.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['SSSP', 'Aho-Corasick', 'Random Tree Classifier'],
                correct_answer='Random Tree Classifier'
            )
            mcq.save()

            qn = Question(
                title='Risheng is...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Django Course created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            partner = Partner.objects.all()[2]

            c = Course(
                title='Next.js Firebase - The Full Course',
                learning_objectives=['Custom Firebase usernames', 'Bot-friendly content (SEO)', 'Advanced SSR, SSG, and ISR techniques', 'Firestore realtime CRUD and data modeling', 'Reactive forms with react-hook-form'],
                requirements=['Basic knowledge of web programming', 'Familiarity of JavaScript, HTML, and CSS'],
                description='Next.js Firebase - The Full Course takes you from zero to a production-ready hybrid-rendered webapp. Learn how build a high-performance React app that features realtime data from Firebase and multiple server-side rendering paradigms with Next.js',
                introduction_video_url='https://youtu.be/Sklc_fQBmcs',
                coding_languages=['JS', 'HTML', 'CSS'],
                languages=['ENG'],
                categories=['BE', 'DB', 'FE'],
                is_published=True,
                published_date=timezone.now(),
                pro=True,
                duration=4,
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course4/course4.png', 'rb')))
            c.save()

            # create some fake views
            for u in BaseUser.objects.all():
                EventLog(
                    payload='course view',
                    user=u,
                    course=c
                ).save()
            # end for

            # chapters
            chap = Chapter(
                title='Lecture 1',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Welcome | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/jGwO_UgTS7I'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 2',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Linear Regression and Gradient Descent | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/4b4MUYve_U8'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 3',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Locally Weighted & Logistic Regression | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/het9HFqo1TQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 4',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Perceptron & Generalized Linear Model | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/iZTeva0WSTQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 5',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='GDA & Naive Bayes | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/nt63k3bfXS0'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 6',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Lecture 6 - Support Vector Machines | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/lDwow4aOrtg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 7',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Kernels | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/8NYoQiRANpg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 8',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title=' Data Splits, Models & Cross-Validation | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/rjbkWSTjHzM'
            )
            cv.save()

            qb = QuestionBank(
                label='Easy',
                course=c,
            )
            qb.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['SSSP', 'Aho-Corasick', 'Random Tree Classifier'],
                correct_answer='Random Tree Classifier'
            )
            mcq.save()

            qn = Question(
                title='Risheng is...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Next Course created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            partner = Partner.objects.all()[2]

            c = Course(
                title='Docker Basics Tutorial with Node.js',
                learning_objectives=['Custom Firebase usernames', 'Bot-friendly content (SEO)', 'Advanced SSR, SSG, and ISR techniques', 'Firestore realtime CRUD and data modeling', 'Reactive forms with react-hook-form'],
                requirements=['Basic knowledge of web programming', 'Familiarity of JavaScript, HTML, and CSS'],
                description='Learn the fundamentals of Docker by containerizing a Node.js app',
                introduction_video_url='https://youtu.be/Sklc_fQBmcs',
                coding_languages=['JS', 'HTML', 'CSS'],
                languages=['ENG'],
                categories=['BE', 'DB', 'FE'],
                is_published=True,
                published_date=timezone.now(),
                pro=False,
                duration=9,
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course5/course5.png', 'rb')))
            c.save()

            # create some fake views
            for u in BaseUser.objects.all():
                EventLog(
                    payload='course view',
                    user=u,
                    course=c
                ).save()
            # end for

            # chapters
            chap = Chapter(
                title='Lecture 1',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Welcome | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/jGwO_UgTS7I'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 2',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Linear Regression and Gradient Descent | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/4b4MUYve_U8'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 3',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Locally Weighted & Logistic Regression | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/het9HFqo1TQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 4',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Perceptron & Generalized Linear Model | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/iZTeva0WSTQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 5',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='GDA & Naive Bayes | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/nt63k3bfXS0'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 6',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Lecture 6 - Support Vector Machines | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/lDwow4aOrtg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 7',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Kernels | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/8NYoQiRANpg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 8',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title=' Data Splits, Models & Cross-Validation | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/rjbkWSTjHzM'
            )
            cv.save()

            qb = QuestionBank(
                label='Easy',
                course=c,
            )
            qb.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['SSSP', 'Aho-Corasick', 'Random Tree Classifier'],
                correct_answer='Random Tree Classifier'
            )
            mcq.save()

            qn = Question(
                title='Risheng is...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Docker Course created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except
        try:
            partner = Partner.objects.all()[2]

            c = Course(
                title='Information Security',
                learning_objectives=['Introduction to Security', 'Threats, vulnerabilities and control'],
                requirements=['Basic knowledge of web programming', 'Familiarity of JavaScript, HTML, and CSS'],
                description='This is a crash course on information security for beginners. It will provide you the basics knowledge and terminology about information security.',
                introduction_video_url='https://www.youtube.com/watch?v=0vvUkancccU',
                coding_languages=['CPP', 'CS'],
                languages=['ENG'],
                categories=['BE', 'DB', 'FE', 'SEC'],
                is_published=True,
                published_date=timezone.now(),
                pro=True,
                duration=9,
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course6/course6.png', 'rb')))
            c.save()

            # create some fake views
            for u in BaseUser.objects.all():
                EventLog(
                    payload='course view',
                    user=u,
                    course=c
                ).save()
            # end for

            # chapters
            chap = Chapter(
                title='Lecture 1',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Welcome | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/jGwO_UgTS7I'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 2',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Linear Regression and Gradient Descent | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/4b4MUYve_U8'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 3',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Locally Weighted & Logistic Regression | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/het9HFqo1TQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 4',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Perceptron & Generalized Linear Model | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/iZTeva0WSTQ'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 5',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='GDA & Naive Bayes | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/nt63k3bfXS0'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 6',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Lecture 6 - Support Vector Machines | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/lDwow4aOrtg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 7',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title='Kernels | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/8NYoQiRANpg'
            )
            cv.save()

            chap = Chapter(
                title='Lecture 8',
                overview='Take an adapted version of this course as part of the Stanford Artificial Intelligence Professional Program. Learn more at the official website.',
                course=c,
                order=c.chapters.count()
            )
            chap.save()

            cm = CourseMaterial(
                title=' Data Splits, Models & Cross-Validation | Stanford CS229: Machine Learning (Autumn 2018)',
                description='',
                material_type='VIDEO',
                order=chap.course_materials.count(),
                chapter=chap,
            )
            cm.save()

            cv = Video(
                course_material=cm,
                video_url='https://youtu.be/rjbkWSTjHzM'
            )
            cv.save()

            qb = QuestionBank(
                label='Easy',
                course=c,
            )
            qb.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mcq = MCQ(
                question=qn,
                marks=1,
                options=['SSSP', 'Aho-Corasick', 'Random Tree Classifier'],
                correct_answer='Random Tree Classifier'
            )
            mcq.save()

            qn = Question(
                title='Risheng is...',
                order=qb.questions.count(),
                question_bank=qb
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qb2 = QuestionBank(
                label='Hard',
                course=c,
            )
            qb2.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=qb2.questions.count(),
                question_bank=qb2
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qg = QuestionGroup(
                count=2,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb
            )
            qg.save()

            qg = QuestionGroup(
                count=1,
                order=q.question_groups.count() + 1,
                quiz=q,
                question_bank=qb2
            )
            qg.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Infosec Course created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # create course comments
        self.stdout.write('Creating some comments...')
        try:
            chap = Chapter.objects.get(title='React Native App Basics')

            user = BaseUser.objects.get(first_name='Steve')
            cm = chap.course_materials.all()[1]
            cc = CourseComment(
                display_id=cm.course_comments.count() + 1,
                comment='This is great!!!',
                course_material=cm,
                user=user,
            )
            cc.save()

            m2 = BaseUser.objects.get(email="m2@m2.com")
            cm = chap.course_materials.all()[1]
            cc = CourseComment(
                display_id=cm.course_comments.count() + 1,
                comment='Would be great if we could copy the code from the video..',
                course_material=cm,
                user=m2,
            )
            cc.save()

            cm = Course.objects.get(title='Stanford CS229: Machine Learning (Autumn 2018)').chapters.all()[0].course_materials.all()[0]
            cc = CourseComment(
                display_id=cm.course_comments.count() + 1,
                comment='This is awesome!!!',
                course_material=cm,
                user=user,
            )
            cc.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Course comments created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # create course consults
        self.stdout.write('Creating some consultations...')
        try:
            p = Partner.objects.get(user__first_name='Andrew')
            m = Member.objects.get(user__email='m1@m1.com')
            now = timezone.now()

            cs = ConsultationSlot(
                title='React Native 0.5',
                start_time=(now + timedelta(minutes=20)),
                end_time=(now + timedelta(minutes=60)),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=0,
                max_members=2,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 1',
                start_time=(now + timedelta(days=1)).replace(hour=2, minute=0),
                end_time=(now + timedelta(days=1)).replace(hour=2, minute=30),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=0,
                max_members=2,
                partner=p
            )
            cs.save()
            
            ConsultationApplication(
                member=m,
                consultation_slot=cs
            ).save()

            cs = ConsultationSlot(
                title='React Native 2',
                start_time=(now + timedelta(days=1)).replace(hour=3, minute=0),
                end_time=(now + timedelta(days=1)).replace(hour=4, minute=0),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=5,
                max_members=2,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 3',
                start_time=(now + timedelta(days=4)).replace(hour=10, minute=0),
                end_time=(now + timedelta(days=4)).replace(hour=11, minute=30),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=0,
                max_members=2,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 4',
                start_time=(now + timedelta(days=4)).replace(hour=8, minute=0),
                end_time=(now + timedelta(days=4)).replace(hour=9, minute=0),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=10,
                max_members=1,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 5',
                start_time=(now + timedelta(days=3)).replace(hour=1, minute=0),
                end_time=(now + timedelta(days=3)).replace(hour=1, minute=30),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=0,
                max_members=1,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 6',
                start_time=(now + timedelta(days=6)).replace(hour=7, minute=20),
                end_time=(now + timedelta(days=6)).replace(hour=9, minute=20),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=10,
                max_members=10,
                partner=p
            )
            cs.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Course consultations created')

            # generate some search stats
            self.stdout.write('Generating some search stats...')
            searches = ['web', 'react native', 'docker', 'django']
            for i in range(99):
                EventLog(
                    payload='search course',
                    search_string=searches[randint(0, 3)]
                ).save()
            # end for
            searches = ['ui designer', 'frontend dev', 'devops engineer', 'ML sexpert']
            for i in range(99):
                EventLog(
                    payload='search industry project',
                    search_string=searches[randint(0, 3)]
                ).save()
            # end for
            self.stdout.write(f'{self.style.SUCCESS("Success")}: Mock search stats initiated')

            # generate event logs for courses
            self.stdout.write('Generating course-related event logs...')
            members = BaseUser.objects.exclude(member=None).all()
            for cm in CourseMaterial.objects.all():
                for i in range(4):
                    EventLog(
                        payload='continue course material',
                        user=members[randint(0, 1)],
                        course_material=cm
                    ).save()
                    EventLog(
                        payload='stop course material',
                        user=members[randint(0, 1)],
                        course_material=cm,
                        duration=randint(60, 2400),
                    ).save()
                # end for
            # end for

            # make a cm really long
            chap = Chapter.objects.get(title='React Native App Basics')
            cm = chap.course_materials.all()[1]
            for i in range(10):
                EventLog(
                    payload='continue course material',
                    user=members[randint(0, 1)],
                    course_material=cm
                ).save()
                EventLog(
                    payload='stop course material',
                    user=members[randint(0, 1)],
                    course_material=cm,
                    duration=randint(1200, 3600),
                ).save()
            # end for
            self.stdout.write(f'{self.style.SUCCESS("Success")}: Event logs initiated')

        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            # initiate some industry projects
            self.stdout.write('Initiating some industry projects...')
            now = timezone.now()
            p = Partner.objects.get(user__email='ep2@ep2.com')

            ip = IndustryProject(
                title='Finance Dashboard',
                description='Build a dashboard using the MERN stack',
                start_date=now + timedelta(days=120),
                end_date=now + timedelta(days=240),
                application_deadline=now + timedelta(days=60),
                categories=['FE', 'BE'],
                partner=p,
            )
            ip.save()

            for i in range(3, 25):
                m = Member.objects.get(user__email=f'm{i}@m{i}.com')
                IndustryProjectApplication(
                    member=m,
                    industry_project=ip
                ).save()
            # end for

            for i in range(1, 31):
                m = Member.objects.get(user__email=f'm{i}@m{i}.com')
                EventLog(
                    payload='view industry project',
                    user=m.user,
                    industry_project=ip
                ).save()
            # end for

            ip = IndustryProject(
                title='Finetune our ranking algorithm!',
                description='Flex your ML skills! KNN!',
                start_date=now + timedelta(days=140),
                end_date=now + timedelta(days=300),
                application_deadline=now + timedelta(days=20),
                categories=['ML', 'BE'],
                partner=p,
            )
            ip.save()

            for i in range(20, 31):
                m = Member.objects.get(user__email=f'm{i}@m{i}.com')
                IndustryProjectApplication(
                    member=m,
                    industry_project=ip
                ).save()
            # end for

            for i in range(1, 31):
                m = Member.objects.get(user__email=f'm{i}@m{i}.com')
                EventLog(
                    payload='view industry project',
                    user=m.user,
                    industry_project=ip
                ).save()
            # end for

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Industry projects initiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            # initiate some articles
            self.stdout.write('Initiating some articles...')
            now = timezone.now()

            ep1 = BaseUser.objects.get(email='ep1@ep1.com')
            ep2 = BaseUser.objects.get(email='ep2@ep2.com')

            a = Article(
                content='''<h2>Building Full Stack dApps with React, Ethers.js, Solidity, and Hardhat</h2><blockquote>The code for this project is located&nbsp;<a href=\"https://github.com/dabit3/full-stack-ethereum\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">here</a></blockquote><p>I recently joined&nbsp;<a href=\"https://twitter.com/edgeandnode\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Edge &amp; Node</a>&nbsp;as a Developer Relations Engineer and have been diving deeper into smart contract development with Ethereum. I have settled upon what I think is the best stack for building full stack dApps with Solidity:</p><p>▶︎ Client Framework -&nbsp;<strong>React</strong></p><p>▶︎ Ethereum development environment -&nbsp;<a href=\"https://hardhat.org/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><strong>Hardhat</strong></a></p><p>▶︎ Ethereum Web Client Library -&nbsp;<a href=\"https://docs.ethers.io/v5/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><strong>Ethers.js</strong></a></p><p>▶︎ API layer -&nbsp;<a href=\"https://thegraph.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">The Graph Protocol</a></p><p>The problem that I ran into though while learning this was that while there was fairly good documentation out there for each of these things individually, there was nothing really out there for how to put all of these things together and understand how they worked with each other. There are some really good boilerplates out there like&nbsp;<a href=\"https://github.com/austintgriffith/scaffold-eth\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">scaffold-eth</a>&nbsp;(which also includes Ethers, Hardhat, and The Graph), but may be too much to pick up for people just getting started.</p><p>I wanted an end to end guide to show me how to build full stack Ethereum apps using the most up to date resources, libraries, and tooling.</p><p>The things I was interested in were this:</p><ol><li>How to create, deploy, and test Ethereum smart contracts to local, test, and mainnet</li><li>How to switch between local, test, and production environments / networks</li><li>How to connect to and interact with the contracts using various environments from a front end like React, Vue, Svelte, or Angular</li></ol><p>After spending some time figuring all of this out and getting going with the stack that I felt really happy with, I thought it would be nice to write up how to build and test a full stack Ethereum app using this stack not only for other people out there who may be interested in this stack, but also for myself for future reference. This is that reference.</p><h2>The pieces</h2><p>Let's go over the main pieces we will be using and how they fit into the stack.</p><h3>1. Ethereum development environment</h3><p>When building smart contracts, you will need a way to deploy your contracts, run tests, and debug Solidity code without dealing with live environments.</p><p>You will also need a way to compile your Solidity code into code that can be run in a client-side application –&nbsp;in our case, a React app. We'll learn more about how this works a little later.</p><p>Hardhat is an Ethereum development environment and framework designed for full stack development and is the framework that I will be using for this tutorial.</p><p>Other similar tools in the ecosystem are&nbsp;<a href=\"https://www.trufflesuite.com/ganache\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Ganache</a>&nbsp;and&nbsp;<a href=\"https://www.trufflesuite.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Truffle</a>.</p><h3>2. Ethereum Web Client Library</h3><p>In our React app, we will need a way to interact with the smart contracts that have been deployed. We will need a way to read for data as well as send new transactions.</p><p><a href=\"https://docs.ethers.io/v5/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">ethers.js</a>&nbsp;aims to be a complete and compact library for interacting with the Ethereum Blockchain and its ecosystem from client-side JavaScript applications like React, Vue, Angular, or Svelte. It is the library we'll be using.</p><p>Another popular option in the ecosystem is&nbsp;<a href=\"https://web3js.readthedocs.io/en/v1.3.4/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">web3.js</a></p><h3>3. Metamask</h3><p><a href=\"https://metamask.io/download.html\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Metamask</a>&nbsp;helps to handle account management and connecting the current user to the blockchain. MetaMask enables users to manage their accounts and keys in a few different ways while isolating them from the site context.</p><p>Once a user has connected their MetaMask wallet, you as a developer can interact with the globally available Ethereum API (<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">window.ethereum</code>) that identifies the users of web3-compatible browsers (like MetaMask users), and whenever you request a transaction signature, MetaMask will prompt the user in as comprehensible a way as possible.</p><h3>4. React</h3><p>React is a front end JavaScript library for building web applications, user interfaces, and UI components. It's maintained by Facebook and many many individual developers and companies.</p><p>React and its large ecosystem of metaframeworks like&nbsp;<a href=\"https://nextjs.org/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Next.js</a>,&nbsp;<a href=\"https://www.gatsbyjs.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Gatsby</a>,&nbsp;<a href=\"https://redwoodjs.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Redwood</a>,&nbsp;<a href=\"https://blitzjs.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Blitz.js</a>, and others enable all types of deployment targets including traditional SPAs, static site generators, server-side rendering, and a combination of all three. React continues to be seemingly dominating the front-end space and I think will continue to do so for at least the near future.</p><h3>5. The Graph</h3><p>For most apps built on blockchains like Ethereum, it's hard and time-intensive to read data directly from the chain, so you used to see people and companies building their own centralized indexing server and serving API requests from these servers. This requires a lot of engineering and hardware resources and breaks the security properties required for decentralization.</p><p>The Graph is an indexing protocol for querying blockchain data that enables the creation of fully decentralized applications and solves this problem, exposing a rich GraphQL query layer that apps can consume. In this guide we won't be building a subgraph for our app but will do so in a future tutorial.</p><h2>What we will be building</h2><p>In this tutorial, we'll be building, deploying, and connecting to a couple of basic smart contracts:</p><ol><li>A contract for creating and updating a message on the Ethereum blockchain</li><li>A contract for minting tokens, then allowing the owner of the contract to send tokens to others and to read the token balances, and for owners of the new tokens to also send them to others.</li></ol><p>We will also build out a React front end that will allow a user to:</p><ol><li>Read the greeting from the contract deployed to the blockchain</li><li>Update the greeting</li><li>Send the newly minted tokens from their address to another address</li><li>Once someone has received tokens, allow them to also send their tokens to someone else</li><li>Read the token balance from the contract deployed to the blockchain</li></ol><h3>Prerequisites</h3><ol><li>Node.js installed on your local machine</li><li><a href=\"https://metamask.io/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">MetaMask</a>&nbsp;Chrome extension installed in your browser</li></ol><p>You do not need to own any Ethereum for this guide as we will be using fake / test Ether on a test network for the entire tutorial.</p><h2>Getting started</h2><p>To get started, we'll create a new React application:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx create-react-app react-dapp\n</pre><p><br></p><p>Next, change into the new directory and install&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\"><a href=\"https://docs.ethers.io/v5/\" rel=\"noopener noreferrer\" target=\"_blank\">ethers.js</a></code>&nbsp;and&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\"><a href=\"https://github.com/nomiclabs/hardhat\" rel=\"noopener noreferrer\" target=\"_blank\">hardhat</a></code>&nbsp;using either&nbsp;<strong>NPM</strong>&nbsp;or&nbsp;<strong>Yarn</strong>:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npm install ethers hardhat @nomiclabs/hardhat-waffle ethereum-waffle chai @nomiclabs/hardhat-ethers\n</pre><p><br></p><h3>Installing &amp; configuring an Ethereum development environment</h3><p>Next, initialize a new Ethereum Development Environment with Hardhat:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx hardhat\n\n? What do you want to do? Create a sample project\n? Hardhat project root: &lt;Choose default path&gt;\n</pre><p><br></p><p>Now you should see the following artifacts created for you in your root directory:</p><p><strong>hardhat.config.js</strong>&nbsp;- The entirety of your Hardhat setup (i.e. your config, plugins, and custom tasks) is contained in this file.</p><p><strong>scripts</strong>&nbsp;- A folder containing a script named&nbsp;<strong>sample-script.js</strong>&nbsp;that will deploy your smart contract when executed</p><p><strong>test</strong>&nbsp;- A folder containing an example testing script</p><p><strong>contracts</strong>&nbsp;- A folder holding an example Ethereum smart contract</p><p>Because of&nbsp;<a href=\"https://hardhat.org/metamask-issue.html\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">a MetaMask configuration issue</a>, we need to update the chain ID on our HardHat configuration to be&nbsp;<strong>1337</strong>. We also need to update the location for the&nbsp;<a href=\"https://hardhat.org/guides/compile-contracts.html#artifacts\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">artifacts</a>&nbsp;for our compiled contracts to be in the&nbsp;<strong>src</strong>&nbsp;directory of our React app.</p><p>To make these updates, open&nbsp;<strong>hardhat.config.js</strong>&nbsp;and update the&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">module.exports</code>&nbsp;to look like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">module.exports = {\n  solidity: \"0.8.3\",\n  paths: {\n    artifacts: './src/artifacts',\n  },\n  networks: {\n    hardhat: {\n      chainId: 1337\n    }\n  }\n};\n</pre><p><br></p><h2>Our smart contract</h2><p>Next, let's have a look at the example contract given to us at&nbsp;<strong>contracts/Greeter.sol</strong>:</p><pre class=\"ql-syntax\" spellcheck=\"false\">//SPDX-License-Identifier: Unlicense\npragma solidity ^0.7.0;\n\nimport \"hardhat/console.sol\";\n\n\ncontract Greeter {\n  string greeting;\n\n  constructor(string memory _greeting) {\n    console.log(\"Deploying a Greeter with greeting:\", _greeting);\n    greeting = _greeting;\n  }\n\n  function greet() public view returns (string memory) {\n    return greeting;\n  }\n\n  function setGreeting(string memory _greeting) public {\n    console.log(\"Changing greeting from '%s' to '%s'\", greeting, _greeting);\n    greeting = _greeting;\n  }\n}\n</pre><p><br></p><p>This is a very basic smart contract. When deployed, it sets a Greeting variable and exposes a function (<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">greet</code>) that can be called to return the greeting.</p><p>It also exposes a function that allows a user to update the greeting (<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">setGreeting</code>). When deployed to the Ethereum blockchain, these methods will be available for a user to interact with.</p><p>Let's make one small modification to the smart contract. Since we set the solidity version of our compiler to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">0.8.3</code>&nbsp;in&nbsp;<strong>hardhat.config.js</strong>, let's also be sure to update our contract to use the same version of solidity:</p><pre class=\"ql-syntax\" spellcheck=\"false\">// contracts/Greeter.sol\npragma solidity ^0.8.3;\n</pre><p><br></p><h3>Reading and writing to the Ethereum blockchain</h3><p>There are two types of ways to interact with a smart contract, reading or writing / transactions. In our contract,&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">greet</code>&nbsp;can be considered reading, and&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">setGreeting</code>&nbsp;can be considered writing / transactional.</p><p>When writing or initializing a transaction, you have to pay for the transaction to be written to the blockchain. To make this work, you need to pay&nbsp;<a href=\"https://www.investopedia.com/terms/g/gas-ethereum.asp#:~:text=What%20Is%20Gas%20(Ethereum)%3F,on%20the%20Ethereum%20blockchain%20platform\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">gas</a>&nbsp;which is the fee, or price, required to successfully conduct a transaction and execute a contract on the Ethereum blockchain.</p><p>As long as you are only reading from the blockchain and not changing or updating anything, you don't need to carry out a transaction and there will be no gas or cost to do so. The function you call is then carried out only by the node you are connected to, so you don't need to pay any gas and the read is free.</p><p>From our React app, the way that we will interact with the smart contract is using a combination of the&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">ethers.js</code>&nbsp;library, the contract address, and the&nbsp;<a href=\"https://docs.soliditylang.org/en/v0.5.3/abi-spec.html\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">ABI</a>&nbsp;that will be created from the contract by hardhat.</p><p>What is an ABI? ABI stands for application binary interface. You can think of it as the interface between your client-side application and the Ethereum blockchain where the smart contract you are going to be interacting with is deployed.</p><p>ABIs are typically compiled from Solidity smart contracts by a development framework like HardHat. You can also often find the ABIs for a smart contract on&nbsp;<a href=\"https://etherscan.io/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Etherscan</a></p><h3>Compiling the ABI</h3><p>Now that we have gone over the basic smart contract and know what ABIs are, let's compile an ABI for our project.</p><p>To do so, go to the command line and run the following command:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx hardhat compile\n</pre><p><br></p><p>Now, you should see a new folder named&nbsp;<strong>artifacts</strong>&nbsp;in the&nbsp;<strong>src</strong>&nbsp;directory. The&nbsp;<strong>artifacts/contracts/Greeter.json</strong>&nbsp;file contains the ABI as one of the properties. When we need to use the ABI, we can import it from our JavaScript file:</p><pre class=\"ql-syntax\" spellcheck=\"false\">import Greeter from './artifacts/contracts/Greeter.sol/Greeter.json'\n</pre><p><br></p><p>We can then reference the ABI like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">console.log(\"Greeter ABI: \", Greeter.abi)\n</pre><p><br></p><blockquote>Note that Ethers.js also enables&nbsp;<a href=\"https://blog.ricmoo.com/human-readable-contract-abis-in-ethers-js-141902f4d917\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">human readable ABIs</a>, but will will not be going into this during this tutorial.</blockquote><h3>Deploying and using a local network / blockchain</h3><p>Next, let's deploy our smart contract to a local blockchain so that we can test it out.</p><p>To deploy to the local network, you first need to start the local test node. To do so, open the CLI and run the following command:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx hardhat node\n</pre><p><br></p><p>When we run this command, you should see a list of addresses and private keys.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--A_zc2Dpd--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/e176nc82ik77hei3a48s.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--A_zc2Dpd--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/e176nc82ik77hei3a48s.jpg\" alt=\"Hardhat node addresses\"></a></p><p>These are 20 test accounts and addresses created for us that we can use to deploy and test our smart contracts. Each account is also loaded up with 10,000 fake Ether. In a moment, we'll learn how to import the test account into MetaMask so that we can use it.</p><p>Next, we need to deploy the contract to the test network. First update the name of&nbsp;<strong>scripts/sample-script.js</strong>&nbsp;to&nbsp;<strong>scripts/deploy.js</strong>.</p><p>Now we can run the deploy script and give a flag to the CLI that we would like to deploy to our local network:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx hardhat run scripts/deploy.js --network localhost\n</pre><p><br></p><p>Once this script is executed, the smart contract should be deployed to the local test network and we should be then able to start interacting with it.</p><blockquote>When the contract was deployed, it used the first account that was created when we started the local network.</blockquote><p>If you look at the output from the CLI, you should be able to see something like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">Greeter deployed to: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0\n</pre><p><br></p><p>This address is what we will use in our client application to talk to the smart contract. Keep this address available as we will need to use it when connecting to it from the client application.</p><p>To send transactions to the smart contract, we will need to connect our MetaMask wallet using one of the accounts created when we ran&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">npx hardhat node</code>. In the list of contracts that the CLI logs out, you should see both an&nbsp;<strong>Account number</strong>&nbsp;as well as a&nbsp;<strong>Private Key</strong>:</p><pre class=\"ql-syntax\" spellcheck=\"false\">➜  react-defi-stack git:(main) npx hardhat node\nStarted HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/\n\nAccounts\n========\nAccount #0: 0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266 (10000 ETH)\nPrivate Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80\n\n...\n</pre><p><br></p><p>We can import this account into MetaMask in order to start using some of the fake Eth available there. To do so, first open MetaMask and update the network to be Localhost 8545:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--UIsqf9Wh--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qnbsbcm4y1md6cwjttpx.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--UIsqf9Wh--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qnbsbcm4y1md6cwjttpx.jpg\" alt=\"MetaMask Localhost\"></a></p><p>Next, in MetaMask click on&nbsp;<strong>Import Account</strong>&nbsp;from the accounts menu:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--rUGcfvYR--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n7vbzlov869gwk9rtwl1.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--rUGcfvYR--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n7vbzlov869gwk9rtwl1.jpg\" alt=\"Import account\"></a></p><p>Copy then paste one of the&nbsp;<strong>Private Keys</strong>&nbsp;logged out by the CLI and click&nbsp;<strong>Import</strong>. Once the account is imported, you should see the Eth in the account:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s---AfAcDFH--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x5lob4yug3jznhy9z0qt.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s---AfAcDFH--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x5lob4yug3jznhy9z0qt.jpg\" alt=\"Imported account\"></a></p><p>Now that we have a smart contract deployed and an account ready to use, we can start interacting with it from the React app.</p><h3>Connecting the React client</h3><p>In this tutorial we are not going to be worrying about building a beautiful UI with CSS and all of that, we are focused 100% on the core functionality to get you up and running. From there, you can take it and make it look good if you'd like.</p><p>With that being said, let's review the two objectives that we want from our React application:</p><ol><li>Fetch the current value of&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">greeting</code>&nbsp;from the smart contract</li><li>Allow a user to update the value of the&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">greeting</code></li></ol><p>With those things being understood, how do we accomplish this? Here are the things we need to do to make this happen:</p><ol><li>Create an input field and some local state to manage the value of the input (to update the&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">greeting</code>)</li><li>Allow the application to connect to the user's MetaMask account to sign transactions</li><li>Create functions for reading and writing to the smart contract</li></ol><p>To do this, open&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">src/App.js</code>&nbsp;and update it with the following code, setting the value of&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">greeterAddress</code>&nbsp;to the address of your smart contract.:</p><pre class=\"ql-syntax\" spellcheck=\"false\">import './App.css';\nimport { useState } from 'react';\nimport { ethers } from 'ethers'\nimport Greeter from './artifacts/contracts/Greeter.sol/Greeter.json'\n\n// Update with the contract address logged out to the CLI when it was deployed \nconst greeterAddress = \"your-contract-address\"\n\nfunction App() {\n  // store greeting in local state\n  const [greeting, setGreetingValue] = useState()\n\n  // request access to the user's MetaMask account\n  async function requestAccount() {\n    await window.ethereum.request({ method: 'eth_requestAccounts' });\n  }\n\n  // call the smart contract, read the current greeting value\n  async function fetchGreeting() {\n    if (typeof window.ethereum !== 'undefined') {\n      const provider = new ethers.providers.Web3Provider(window.ethereum)\n      const contract = new ethers.Contract(greeterAddress, Greeter.abi, provider)\n      try {\n        const data = await contract.greet()\n        console.log('data: ', data)\n      } catch (err) {\n        console.log(\"Error: \", err)\n      }\n    }    \n  }\n\n  // call the smart contract, send an update\n  async function setGreeting() {\n    if (!greeting) return\n    if (typeof window.ethereum !== 'undefined') {\n      await requestAccount()\n      const provider = new ethers.providers.Web3Provider(window.ethereum);\n      const signer = provider.getSigner()\n      const contract = new ethers.Contract(greeterAddress, Greeter.abi, signer)\n      const transaction = await contract.setGreeting(greeting)\n      await transaction.wait()\n      fetchGreeting()\n    }\n  }\n\n  return (\n    &lt;div className=\"App\"&gt;\n      &lt;header className=\"App-header\"&gt;\n        &lt;button onClick={fetchGreeting}&gt;Fetch Greeting&lt;/button&gt;\n        &lt;button onClick={setGreeting}&gt;Set Greeting&lt;/button&gt;\n        &lt;input onChange={e =&gt; setGreetingValue(e.target.value)} placeholder=\"Set greeting\" /&gt;\n      &lt;/header&gt;\n    &lt;/div&gt;\n  );\n}\n\nexport default App;\n</pre><p><br></p><p>To test it out, start the React server:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npm start\n</pre><p><br></p><p>When the app loads, you should be able to fetch the current greeting and log it out to the console. You should also be able to make updates to the greeting by signing the contract with your MetaMask wallet and spending the fake Ether.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--AWIvD2l3--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9a57jbzrwylr2l0rujxm.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--AWIvD2l3--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9a57jbzrwylr2l0rujxm.png\" alt=\"Setting and getting the greeting value\"></a></p><h3>Deploying and using a live test network</h3><p>There are several Ethereum test networks like Ropsten, Rinkeby, or Kovan that we can also deploy to in order to have a publicly accessible version of our contract available without having to deploy it to mainnet. In this tutorial we'll be deploying to the&nbsp;<strong>Ropsten</strong>&nbsp;test network.</p><p>To start off, first update your MetaMask wallet to connect to the Ropsten network.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--HSvy3DUN--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k85gplgp26wp58l95bhr.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--HSvy3DUN--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k85gplgp26wp58l95bhr.jpg\" alt=\"Ropsten network\"></a></p><p>Next, send yourself some test Ether to use during the rest of this tutorial by visiting&nbsp;<a href=\"https://faucet.ropsten.be/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">this test faucet</a>.</p><p>We can get access to Ropsten (or any of the other test networks) by signing up with a service like&nbsp;<a href=\"https://infura.io/dashboard/ethereum/cbdf7c5eee8b4e2b91e76b77ffd34533/settings\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Infura</a>&nbsp;or&nbsp;<a href=\"https://www.alchemyapi.io/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Alchemy</a>&nbsp;(I'm using Infura for this tutorial).</p><p>Once you've created the app in Infura or Alchemy, you will be given an endpoint that looks something like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">https://ropsten.infura.io/v3/your-project-id\n</pre><p><br></p><p>Be sure to set the&nbsp;<strong>ALLOWLIST ETHEREUM ADDRESSES</strong>&nbsp;in the Infura or Alchemy app configuration to include the wallet address of the account you will be deploying from.</p><p>To deploy to the test network we need to update our hardhat config with some additional network information. One of the things we need to set is the private key of the wallet we will be deploying from.</p><p>To get the private key, you can export it from MetaMask.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--_g7R_Fdh--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/deod3d6qix8us12t17i4.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--_g7R_Fdh--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/deod3d6qix8us12t17i4.jpg\" alt=\"Export private key\"></a></p><blockquote>I'd suggest not hardcoding this value in your app but instead setting it as something like an environment variable.</blockquote><p>Next, add a&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">networks</code>&nbsp;property with the following configuration:</p><pre class=\"ql-syntax\" spellcheck=\"false\">module.exports = {\n  defaultNetwork: \"hardhat\",\n  paths: {\n    artifacts: './src/artifacts',\n  },\n  networks: {\n    hardhat: {},\n    ropsten: {\n      url: \"https://ropsten.infura.io/v3/your-project-id\",\n      accounts: [`0x${your-private-key}`]\n    }\n  },\n  solidity: \"0.7.3\",\n};\n</pre><p><br></p><p>To deploy, run the following script:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx hardhat run scripts/deploy.js --network ropsten\n</pre><p><br></p><p>Once your contract is deployed you should be able to start interacting with it. You should be now able to view the live contract on&nbsp;<a href=\"https://ropsten.etherscan.io/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Etherscan Ropsten Testnet Explorer</a></p><h2>Minting tokens</h2><p>One of the most common use cases of smart contracts is creating tokens, let's look at how we can do that. Since we know a little more about how all of this works, we'll be going a little faster.</p><p>In the main&nbsp;<strong>contracts</strong>&nbsp;directory create a new file named&nbsp;<strong>Token.sol</strong>.</p><p>Next, update&nbsp;<strong>Token.sol</strong>&nbsp;with the following smart contract:</p><pre class=\"ql-syntax\" spellcheck=\"false\">//SPDX-License-Identifier: Unlicense\npragma solidity ^0.8.3;\n\nimport \"hardhat/console.sol\";\n\ncontract Token {\n  string public name = \"Nader Dabit Token\";\n  string public symbol = \"NDT\";\n  uint public totalSupply = 1000000;\n  address public owner;\n  mapping(address =&gt; uint) balances;\n\n  constructor() {\n    balances[msg.sender] = totalSupply;\n    owner = msg.sender;\n  }\n\n  function transfer(address to, uint amount) external {\n    require(balances[msg.sender] &gt;= amount, \"Not enough tokens\");\n    balances[msg.sender] -= amount;\n    balances[to] += amount;\n  }\n\n  function balanceOf(address account) external view returns (uint) {\n    return balances[account];\n  }\n}\n</pre><p><br></p><blockquote>Note that this token contract is for demo purposes only and is not&nbsp;<a href=\"https://eips.ethereum.org/EIPS/eip-20\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">ERC20</a>&nbsp;compliant. For an example of an ERC20 token, check out&nbsp;<a href=\"https://solidity-by-example.org/app/erc20/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">this contract</a></blockquote><p>This contract will create a new token called \"Nader Dabit Token\" and set the supply to 1000000.</p><p>Next, compile this contract:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx hardhat compile\n</pre><p><br></p><p>Now, update the deploy script at&nbsp;<strong>scripts/deploy.js</strong>&nbsp;to include this new Token contract:</p><pre class=\"ql-syntax\" spellcheck=\"false\">const hre = require(\"hardhat\");\n\nasync function main() {\n  const [deployer] = await hre.ethers.getSigners();\n\n  console.log(\n    \"Deploying contracts with the account:\",\n    deployer.address\n  );\n\n  const Greeter = await hre.ethers.getContractFactory(\"Greeter\");\n  const greeter = await Greeter.deploy(\"Hello, World!\");\n\n  const Token = await hre.ethers.getContractFactory(\"Token\");\n  const token = await Token.deploy();\n\n  await greeter.deployed();\n  await token.deployed();\n\n  console.log(\"Greeter deployed to:\", greeter.address);\n  console.log(\"Token deployed to:\", token.address);\n}\n\nmain()\n  .then(() =&gt; process.exit(0))\n  .catch(error =&gt; {\n    console.error(error);\n    process.exit(1);\n  });\n</pre><p><br></p><p>Now, we can deploy this new contract to the local or Ropsten network:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npx run scripts/deploy.js --network localhost\n</pre><p><br></p><p>Once the contract is deployed, you can start sending these tokens to other addresses.</p><p>To do so, let's update the client code we will need in order to make this work:</p><pre class=\"ql-syntax\" spellcheck=\"false\">import './App.css';\nimport { useState } from 'react';\nimport { ethers } from 'ethers'\nimport Greeter from './artifacts/contracts/Greeter.sol/Greeter.json'\nimport Token from './artifacts/contracts/Token.sol/Token.json'\n\nconst greeterAddress = \"your-contract-address\"\nconst tokenAddress = \"your-contract-address\"\n\nfunction App() {\n  const [greeting, setGreetingValue] = useState()\n  const [userAccount, setUserAccount] = useState()\n  const [amount, setAmount] = useState()\n\n  async function requestAccount() {\n    await window.ethereum.request({ method: 'eth_requestAccounts' });\n  }\n\n  async function fetchGreeting() {\n    if (typeof window.ethereum !== 'undefined') {\n      const provider = new ethers.providers.Web3Provider(window.ethereum)\n      console.log({ provider })\n      const contract = new ethers.Contract(greeterAddress, Greeter.abi, provider)\n      try {\n        const data = await contract.greet()\n        console.log('data: ', data)\n      } catch (err) {\n        console.log(\"Error: \", err)\n      }\n    }    \n  }\n\n  async function getBalance() {\n    if (typeof window.ethereum !== 'undefined') {\n      const [account] = await window.ethereum.request({ method: 'eth_requestAccounts' })\n      console.log({ account })\n      const provider = new ethers.providers.Web3Provider(window.ethereum);\n      const signer = provider.getSigner()\n      const contract = new ethers.Contract(tokenAddress, Token.abi, signer)\n      contract.balanceOf(account).then(data =&gt; {\n        console.log(\"data: \", data.toString())\n      })\n    }\n  }\n\n  async function setGreeting() {\n    if (!greeting) return\n    if (typeof window.ethereum !== 'undefined') {\n      await requestAccount()\n      const provider = new ethers.providers.Web3Provider(window.ethereum);\n      console.log({ provider })\n      const signer = provider.getSigner()\n      const contract = new ethers.Contract(greeterAddress, Greeter.abi, signer)\n      const transaction = await contract.setGreeting(greeting)\n      await transaction.wait()\n      fetchGreeting()\n    }\n  }\n\n  async function sendCoins() {\n    if (typeof window.ethereum !== 'undefined') {\n      await requestAccount()\n      const provider = new ethers.providers.Web3Provider(window.ethereum);\n      const signer = provider.getSigner()\n      const contract = new ethers.Contract(tokenAddress, Token.abi, signer)\n      contract.transfer(userAccount, amount).then(data =&gt; console.log({ data }))\n    }\n  }\n\n  return (\n    &lt;div className=\"App\"&gt;\n      &lt;header className=\"App-header\"&gt;\n        &lt;button onClick={fetchGreeting}&gt;Fetch Greeting&lt;/button&gt;\n        &lt;button onClick={setGreeting}&gt;Set Greeting&lt;/button&gt;\n        &lt;input onChange={e =&gt; setGreetingValue(e.target.value)} placeholder=\"Set greeting\" /&gt;\n\n        &lt;br /&gt;\n        &lt;button onClick={getBalance}&gt;Get Balance&lt;/button&gt;\n        &lt;button onClick={sendCoins}&gt;Send Coins&lt;/button&gt;\n        &lt;input onChange={e =&gt; setUserAccount(e.target.value)} placeholder=\"Account ID\" /&gt;\n        &lt;input onChange={e =&gt; setAmount(e.target.value)} placeholder=\"Amount\" /&gt;\n      &lt;/header&gt;\n    &lt;/div&gt;\n  );\n}\n\nexport default App;\n</pre><p><br></p><p>Next, run the app:</p><pre class=\"ql-syntax\" spellcheck=\"false\">npm start\n</pre><p><br></p><p>We should be able to click on&nbsp;<strong>Get Balance</strong>&nbsp;and see that we have 1,000,000 coins in our account logged out to the console.</p><p>You should also be able to view them in MetaMask by clicking on&nbsp;<strong>Add Token</strong>:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--bYhSNJ4P--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0t2ip26i5d2ltjc9j2a6.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--bYhSNJ4P--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0t2ip26i5d2ltjc9j2a6.jpg\" alt=\"Add token\"></a></p><p>Next click on&nbsp;<strong>Custom Token</strong>&nbsp;and enter the token contract address and then&nbsp;<strong>Add Token</strong>. Now the tokens should be available in your wallet:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--tLmPpIH8--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5op32iqbeszizri72qc0.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--tLmPpIH8--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5op32iqbeszizri72qc0.jpg\" alt=\"NDT\"></a></p><p>Next, let's try to send those coins to another address.</p><p>To do so, copy the address of another account and send them to that address using the updated React UI. When you check the token amount, it should be equal to the original amount minus the amount you sent to the address.</p><h2>Conclusion</h2><p>Ok, we covered a lot here but for me this is kind of the bread and butter / core of getting started with this stack and is kind of what I wanted to have not only as someone who was learning all of this stuff, but also in the future if I ever need to reference anything I may need in the future. I hope you learned a lot.</p><p>If you want to support multiple wallets in addition to MetaMask, check out&nbsp;<a href=\"https://github.com/Web3Modal/web3modal\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Web3 Modal</a>&nbsp;which makes it easy to implement support for multiple providers in your app with a fairly simple and customizable configuration.</p><p>In my future tutorials and guides I'll be diving into more complex smart contract development and also how to deploy them as&nbsp;<a href=\"https://thegraph.com/docs/define-a-subgraph\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">subgraphs</a>&nbsp;to expose a GraphQL API on top of them and implement things like pagination and full text search.</p><p>I'll also be going into how to use technologies like IPFS and Web3 databases to store data in a decentralized way.</p><h2>If you have any questions or suggestions for future tutorials, drop some comments here and let me know.</h2>''',
                title='The Complete Guide to Full Stack Ethereum Development',
                coding_languages=['JS'],
                languages=['ENG'],
                categories=['FE'],
                user=ep1,
                is_published=True,
                date_created=now - timedelta(days=2),
            )
            a.thumbnail.save('article1.png', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article1.png', 'rb')))
            a.save()

            a = Article(
                content='''<p>JavaScript is no doubt one of the coolest languages in the world and is gaining more and more popularity day by day. So the developer community has found some tricks and tips after using JS for quite a while now. Today I will share 11 Tips &amp; Tricks With You!</p><p>So let's get started</p><h2>Functional Inheritance</h2><p>Functional inheritance is the process of receiving features by applying an augmenting function to an object instance. The function supplies a closure scope which you can use to keep some data private. The augmenting function uses dynamic object extension to extend the object instance with new properties and methods.</p><p>They look like:</p><pre class=\"ql-syntax\" spellcheck=\"false\">// Base function\nfunction Drinks(data) {\n  var that = {}; // Create an empty object\n  that.name = data.name; // Add it a \"name\" property\n  return that; // Return the object\n};\n\n// Fuction which inherits from the base function\nfunction Coffee(data) {\n  // Create the Drinks object\n  var that = Drinks(data);\n  // Extend base object\n  that.giveName = function() {\n    return 'This is ' + that.name;\n  };\n  return that;\n};\n\n// Usage\nvar firstCoffee = Coffee({ name: 'Cappuccino' });\nconsole.log(firstCoffee.giveName());\n// Output: \"This is Cappuccino\"\n</pre><p><br></p><p>Credits to&nbsp;<a href=\"https://twitter.com/loverajoel\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">@loverajoel</a>&nbsp;for explaining this topic in depth here -&nbsp;<a href=\"https://www.jstips.co/en/javascript/what-is-a-functional-inheritance/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Functional Inheritance on JS Tips</a>&nbsp;which I've paraphrased above</p><h2>.map() Substitute</h2><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">.map()</code>&nbsp;also has a substitute that we can use which is&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">.from()</code>:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let dogs = [\n    { name: ‘Rio’, age: 2 },\n    { name: ‘Mac’, age: 3 },\n    { name: ‘Bruno’, age: 5 },\n    { name: ‘Jucas’, age: 10 },\n    { name: ‘Furr’, age: 8 },\n    { name: ‘Blu’, age: 7 },\n]\n\n\nlet dogsNames = Array.from(dogs, ({name}) =&gt; name);\nconsole.log(dogsNames); // returns [“Rio”, “Mac”, “Bruno”, “Jucas”, “Furr”, “Blu”]\n</pre><p><br></p><h2>Number to string/string to number</h2><p>Usually, to convert a string to a number, we use something like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let num = 4\nlet newNum = num.toString();\n</pre><p><br></p><p>and to convert a string to a number, we use:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let num = \"4\"\nlet stringNumber = Number(num);\n</pre><p><br></p><p>but what we can use to code fast is:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let num = 15;\nlet numString = num + \"\"; // number to string\nlet stringNum = +s; // string to number\n</pre><p><br></p><h2>Using length to resize and emptying an array</h2><p>In javascript, we can override a built-in method called&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">length</code>&nbsp;and assign it a value of our choice.</p><p>Let's look at an example:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let array_values = [1, 2, 3, 4, 5, 6, 7, 8];  \nconsole.log(array_values.length); \n// 8  \narray_values.length = 5;  \nconsole.log(array_values.length); \n// 5  \nconsole.log(array_values); \n// [1, 2, 3, 4, 5]\n</pre><p><br></p><p>It can also be used in emptying an array, like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let array_values = [1, 2, 3, 4, 5, 6, 7,8]; \nconsole.log(array_values.length); \n// 8  \narray_values.length = 0;   \nconsole.log(array_values.length); \n// 0 \nconsole.log(array_values); \n// []\n</pre><p><br></p><h2>Swap Values with Array Destructuring.</h2><p>The&nbsp;<strong>destructuring</strong>&nbsp;assignment syntax is a JavaScript expression that makes it possible to unpack values from arrays, or properties from objects, into distinct variables. We can also use that to swap values fast, like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">let a = 1, b = 2\n[a, b] = [b, a]\nconsole.log(a) // result -&gt; 2\nconsole.log(b) // result -&gt; 1\n</pre><p><br></p><h2>Remove duplicates from an Array</h2><p>This trick is pretty simple. Let's say, I made an array that is containing numbers, strings, and booleans, but the values are repeating themselves more than once and I want to remove the duplicates. So what I can do is:</p><pre class=\"ql-syntax\" spellcheck=\"false\">const array = [1, 3, 2, 3, 2, 1, true, false, true, 'Kio', 2, 3];\nconst filteredArray = [...new Set(array)];\nconsole.log(filteredArray) // [1, 3, 2, true, false, \"Kio\"]\n</pre><p><br></p><h2>Short For Loop</h2><p>You can write less code for a loop like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">const names = [\"Kio\", \"Rio\", \"Mac\"];\n\n// Long Version\nfor (let i = 0; i &lt; names.length; i++) {\n  const name = names[i];\n  console.log(name);\n}\n\n// Short Version\nfor (let name of names) console.log(name);\n</pre><p><br></p><h2>Performance</h2><p>In JS you can also get the time that the code was executed in like Google does:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--JSbC-A0p--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i7ed89oyhcyyjhqirvc6.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--JSbC-A0p--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i7ed89oyhcyyjhqirvc6.png\" alt=\"google example\"></a></p><p>It looks like this:</p><pre class=\"ql-syntax\" spellcheck=\"false\">const firstTime = performance.now();\nsomething();\nconst secondTime = performance.now();\nconsole.log(`The something function took ${secondTime - firstTime} milliseconds.`);\n</pre><p><br></p><p>Thank you very much for reading this article.</p><p>Comment any tricks &amp; tips you know!</p><p><strong>PLEASE LIKE, SHARE, AND COMMENT</strong></p><p>Follow me on&nbsp;<a href=\"https://dev.to/garvitmotwani\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Dev</a>&nbsp;and&nbsp;<a href=\"https://twitter.com/GarvitMotwani\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Twitter</a></p><p>You Should also check</p><p><br></p><h2><a href=\"https://dev.to/devlorenzo\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--QtgKvHIX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://res.cloudinary.com/practicaldev/image/fetch/s--N0bOH9Ja--/c_fill%2Cf_auto%2Cfl_progressive%2Ch_150%2Cq_66%2Cw_150/https://dev-to-uploads.s3.amazonaws.com/uploads/user/profile_image/571015/3b1e2909-e87b-4fc7-b817-0673184568b0.gif\" alt=\"devlorenzo image\">&nbsp;</a><a href=\"https://dev.to/devlorenzo/10-projects-to-become-a-javascript-master-giveaway-2o4k\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Projects to become a javascript master 🚀 Resource compilation 💥 + Giveaway⚡</a></h2><h3><a href=\"https://dev.to/devlorenzo/10-projects-to-become-a-javascript-master-giveaway-2o4k\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">DevLorenzo ・ Apr 10 ・ 7 min read</a></h3><p><a href=\"https://dev.to/devlorenzo/10-projects-to-become-a-javascript-master-giveaway-2o4k\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">#javascript&nbsp;#webdev&nbsp;#programming&nbsp;#beginners</a></p><p>by my friend&nbsp;<a href=\"https://dev.to/devlorenzo\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">@devlorenzo</a></p><p>Subscribe to our&nbsp;<a href=\"https://chipper-motivator-3112.ck.page/05710ea3d3\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">newsletter</a>&nbsp;to receive our weekly recap directly on your email!</p><p>Join us on&nbsp;<a href=\"https://discord.gg/aWS2YKk6\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Discord</a>&nbsp;to participate in hackathons with us / participate in our giveaways!</p><p>Happy Coding.</p>''',
                title='8 JavaScript Tips & Tricks That No One Teaches 🚀',
                coding_languages=['JS'],
                languages=['ENG'],
                categories=['FE'],
                user=ep2,
                is_published=True,
            )
            a.thumbnail.save('article2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article2.jpeg', 'rb')))
            a.save()

            a = Article(
                content='''<h1>Introduction</h1><p>We have a list of various resources that can help you to solve many problems that you are facing or might face in the future.</p><p>We have resources for</p><p><br></p><ul><li>Illustration</li><li>Development</li><li>Design</li><li>CSS</li><li>Productivity</li></ul><p>Let's get started without further ado.</p><p><br></p><p><br></p><h1>ILLUSTRATION</h1><h3><a href=\"https://www.drawkit.io/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Drawit</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--BMNJ-K21--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dsftv9zy5tfo1r1epr8x.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--BMNJ-K21--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dsftv9zy5tfo1r1epr8x.png\" alt=\"DrawKit\"></a></p><blockquote>Hand-drawn vector illustration and icon resources, perfect for your next project.</blockquote><h3><br></h3><h3><a href=\"https://www.flaticon.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">FlatIcon</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--h-0vHQeX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/t7u6kpnrq851g3bln036.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--h-0vHQeX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/t7u6kpnrq851g3bln036.jpg\" alt=\"flaticon-generic\"></a></p><blockquote>4340500+ Free vector icons in SVG, PSD, PNG, EPS format or as ICON FONT. Thousands of free icons in the largest database of free vector icons!</blockquote><h3><br></h3><h3><a href=\"https://blush.design/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Blush Design</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--E7x6tsBf--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uhpfr7xzcgd4kcnpgm0d.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--E7x6tsBf--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uhpfr7xzcgd4kcnpgm0d.png\" alt=\"Blush Design\"></a></p><blockquote>Easily create and customize stunning illustrations with collections made by artists across the globe. Try it, it’s kind of fun.</blockquote><h3><br></h3><h3><a href=\"https://usesmash.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Smash Illustration</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--t0odzE4g--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rqk6zlp1c859v5ffh7uu.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--t0odzE4g--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rqk6zlp1c859v5ffh7uu.png\" alt=\"Smash Illustration\"></a></p><h3><br></h3><h3><a href=\"https://blush.design/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">unDraw</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--ghj0XILl--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9dxgj5o0auvj2d6hv92n.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--ghj0XILl--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9dxgj5o0auvj2d6hv92n.png\" alt=\"unDraw\"></a></p><blockquote>Open-source illustrations for any idea you can imagine and create. A constantly updated design project with beautiful SVG images that you can use completely free and without attribution.</blockquote><blockquote>Awesome illustration constructor with colorful and trendy characters</blockquote><p><br></p><p><br></p><h3><a href=\"https://clockify.me/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Clockify</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--1pJm0fC7--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n7nxv74ukv7fx3xf6pmo.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--1pJm0fC7--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n7nxv74ukv7fx3xf6pmo.png\" alt=\"Clockify\"></a></p><blockquote>The most popular free time tracker for teams. The time tracking software used by millions. Clockify is a simple time tracker and timesheet app that lets you and your team track work hours across projects. Unlimited users, free forever.</blockquote><h3><br></h3><h3><a href=\"https://untools.co/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Untools</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--CBPjPdfz--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hgpuafqr2ohhefqcyu8q.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--CBPjPdfz--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hgpuafqr2ohhefqcyu8q.jpg\" alt=\"Untools\"></a></p><p><br></p><p><br></p><blockquote>Collection of thinking tools and frameworks to help you solve problems, make decisions, and understand systems.</blockquote>''',
                title='40+ Useful Resources for Mastering Web🎁',
                coding_languages=[
                    "JS",
                    "HTML"
                ],
                languages=['ENG'],
                categories=['FE', 'BE', 'UI'],
                user=ep1,
                is_published=True,
            )
            a.thumbnail.save('article3.png', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article3.png', 'rb')))
            a.save()

            a = Article(
                content='''<p>Are you trying to setup your workspace so as to ease your work and boost your productivity? This is for you</p><p>When I started out, there was an overwhelming urge to test out every code editor there was, try out every shortcut and install every extension. Yeah, the excitement was immense!😅.</p><p>Here are some extensions that I have found&nbsp;<em>truly&nbsp;</em><strong>useful</strong>&nbsp;in my learning journey.</p><p><strong>PS:</strong>&nbsp;The text editor used here is visual studio codes...did I say that already?</p><h1>VS Extensions</h1><h3>1.&nbsp;<a href=\"https://www.codereadability.com/automated-code-formatting-with-prettier/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Prettier</a></h3><p>Prettier integrates with your editor, so your code is tidied up every time you save your changes. It makes the code more readable and consistent with your project's style guide.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--vlPzL_jl--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ktbqbq5usntt5vcax5qw.gif\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--vlPzL_jl--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ktbqbq5usntt5vcax5qw.gif\" alt=\"Alt Text\"></a></p><p><a href=\"https://www.codereadability.com/automated-code-formatting-with-prettier/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up Prettier plugin</a></p><h3>2.&nbsp;<a href=\"https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Auto Rename Tag</a></h3><p>This extension saves a lot of time.It automatically renames the closing tag when you rename the opening tag.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--AWi8mxjB--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l299gy61k7phyhs3hrlu.gif\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--AWi8mxjB--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l299gy61k7phyhs3hrlu.gif\" alt=\"Alt Text\"></a></p><p><a href=\"https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><h3>3.&nbsp;<a href=\"https://ritwickdey.github.io/vscode-live-server/#:~:text=Right%20click%20on%20a%20HTML,to%20Open%20with%20Live%20Server%20.&amp;text=Open%20a%20HTML%20file%20and,editor%20and%20choose%20the%20options.&amp;text=Press%20F1%20or%20ctrl%2Bshift,Server%20to%20stop%20a%20server.\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Live server</a></h3><p>This extension automatically refreshes the browser whenever you save your work. It is especially useful when working with html, css and js projects.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--4919ceFg--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6hgj1bxzk7rv8yuosush.gif\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--4919ceFg--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6hgj1bxzk7rv8yuosush.gif\" alt=\"Alt Text\"></a></p><p><a href=\"https://ritwickdey.github.io/vscode-live-server/#:~:text=Right%20click%20on%20a%20HTML,to%20Open%20with%20Live%20Server%20.&amp;text=Open%20a%20HTML%20file%20and,editor%20and%20choose%20the%20options.&amp;text=Press%20F1%20or%20ctrl%2Bshift,Server%20to%20stop%20a%20server.\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><h3>4.&nbsp;<a href=\"https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer-2\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Bracket Pair Colorizer2</a></h3><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--Kk9s-chU--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8hhsiq0ixnqob5m1z0fv.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--Kk9s-chU--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8hhsiq0ixnqob5m1z0fv.png\" alt=\"Alt Text\"></a></p><p>This extension matches a bracket pair with a unique color. You'll find this extension quite useful when browsing through your code especially when you have several scopes deep in your code.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--cUFhSPLr--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w7idah2a865n6h5i8qwq.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--cUFhSPLr--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w7idah2a865n6h5i8qwq.png\" alt=\"Alt Text\"></a></p><p><a href=\"https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer-2\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><h3>5.&nbsp;<a href=\"https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Indent-rainbow</a></h3><p>This extension increases the readability of your code and makes it easy to browse throught your work.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--wOi9yGaf--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0grszgsnbvsdj4qjxvaw.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--wOi9yGaf--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0grszgsnbvsdj4qjxvaw.png\" alt=\"Alt Text\"></a></p><p><a href=\"https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><h3>6.&nbsp;<a href=\"https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Path intellisense</a></h3><p>This extension autocompletes file paths when referencing them in a link.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--4dTkHKz8--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k1sf1hdm8waojdfld4ds.gif\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--4dTkHKz8--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k1sf1hdm8waojdfld4ds.gif\" alt=\"Alt Text\"></a></p><p><a href=\"https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><h3>7.&nbsp;<a href=\"https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Material Icon Theme</a></h3><p>Material Icon Theme makes icons more obvious to the eye. So you can quicky identify different files types from each other.</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--txmaRTlb--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kce9ijygk5g6wide4g5b.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--txmaRTlb--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kce9ijygk5g6wide4g5b.png\" alt=\"Alt Text\"></a></p><p><a href=\"https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><h3>8.&nbsp;<a href=\"https://marketplace.visualstudio.com/search?term=theme&amp;target=VSCode&amp;category=All%20categories&amp;sortBy=Relevance\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Theme</a></h3><p>It's always nice to enjoy your coding experience and you could definitely spice it by adding a theme and the good news is the is a long list from which you could pick according to your taste.</p><p>Personally, I like the&nbsp;<a href=\"https://marketplace.visualstudio.com/items?itemName=whizkydee.material-palenight-theme\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Palenight theme.</a>&nbsp;It's quite elegant😏</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--YE6G_E52--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2ipmwwjacutdiudj6li9.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--YE6G_E52--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2ipmwwjacutdiudj6li9.png\" alt=\"Alt Text\"></a></p><p><a href=\"https://marketplace.visualstudio.com/items?itemName=whizkydee.material-palenight-theme\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">How to set up plugin</a></p><p>Hey this is just a limited list of extensions you can find on VS code, there's so much more out there.</p><p>Comment down below on which extension you found(or think is) most useful as a beginner programmer.</p>''',
                title='VS code extensions to boost productivity (with previews)',
                coding_languages=[
                    "PY",
                    "JAVA",
                    "JS",
                    "CPP",
                    "CS",
                    "HTML",
                    "CSS",
                    "RUBY"
                ],
                languages=['ENG'],
                categories=[
                    "SEC",
                    "DB",
                    "FE",
                    "BE",
                    "UI",
                    "ML"
                ],
                user=ep2,
                is_published=True,
            )
            a.thumbnail.save('article4.gif', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article4.gif', 'rb')))
            a.save()

            a = Article(
                content='''<p>The better way to learn is by getting our hands dirty and building things, let's build a simplified version of the Instagram web application with the awesome PETAL(Phoenix, Elixir, TailwindCSS, AlpineJS, LiveView) stack and deep dive into the dark world of functional programming and hottest kid on the block the Phoenix framework with LiveView.</p><p>I don't consider myself a teacher and no expert at anything, I'm just a regular dude just like you. Anybody can follow along even though you might get intimidated by the whole stack, it's kind of a new technology and not very popular, and not a lot of resources and materials out there. If you are an experienced developer you will have no problem, it doesn't mean that if you're a beginner you cannot follow along, I will do my best to make it beginner friendly but I will not go over every basic of the stack or web development so you've been warned.</p><p>Elixir's one of the best languages that I ever have the pleasure of learning, experimenting with, and I want to share my passion with the world, I want others to feel what I feel for the language.</p><p><strong>Disclaimer:</strong>&nbsp;Elixir, Functional Programming, Phoenix Framework, might sound, look difficult and complicated but it is not at all, is easier than anything else out there, it might not be for everyone because we all do not think alike but for those who think like me will feel as I feel trying it. TailwindCSS might be opinionated, look not worth trying it, I know it because that's how I felt too, but just try it, the more you use it the more sense it will make and the more you will love it, it makes CSS uncomplicated, makes you not give up on front end development, CSS will still be painful, as developers, we don't have the patience that takes to get the UI right but it's a breath of fresh air.</p><p>We will not finish the whole project on this article, it will be a series of articles so this will be part 1. I will assume that you have your own development environment with Elixir installed, my development environment is on Windows 10 with WSL. We will try to be as detail as possible but keeping it simple, it is just for learning purposes only so it will not be an exact copy and it will not have every feature, we will get as close as possible to the real thing, also we will not focus on making the site responsive, we'll just make it work for large screens.</p><p>Let's start by going to the terminal and creating a fresh Phoenix app with LiveView.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ mix phx.new instagram_clone --live</code></p><p>Once all dependencies are installed and fetched.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ cd instagram_clone &amp;&amp; mix ecto.create</code></p><p>I created a GitHub repo that you can visit here&nbsp;<a href=\"https://github.com/elixirprogrammer/InstagramClonePETAL\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Instagram Clone GitHub Repo</a>&nbsp;feel free to use the code as you wish, contributions are welcome.</p><p>Let's run the server to make sure that everything's working.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ iex -S mix phx.server</code></p><p>If no errors you should have the default Phoenix framework homepage when you go to&nbsp;<a href=\"http://localhost:4000/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">http://localhost:4000/</a></p><p>I use Visual Studio Code so I will open the project folder with the following command.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ code .</code></p><p>Now let's add our mix dependencies in our mix.exs file.</p><pre class=\"ql-syntax\" spellcheck=\"false\"># mix.exs file\n\n  defp deps do\n    [\n      {:phoenix, \"~&gt; 1.5.6\"},\n      {:phoenix_ecto, \"~&gt; 4.1\"},\n      {:ecto_sql, \"~&gt; 3.4\"},\n      {:postgrex, \"&gt;= 0.0.0\"},\n      {:floki, \"&gt;= 0.27.0\", only: :test},\n      {:phoenix_html, \"~&gt; 2.11\"},\n      {:phoenix_live_reload, \"~&gt; 1.2\", only: :dev},\n      {:phoenix_live_dashboard, \"~&gt; 0.3 or ~&gt; 0.2.9\"},\n      {:telemetry_metrics, \"~&gt; 0.4\"},\n      {:telemetry_poller, \"~&gt; 0.4\"},\n      {:gettext, \"~&gt; 0.11\"},\n      {:jason, \"~&gt; 1.0\"},\n      {:plug_cowboy, \"~&gt; 2.0\"},\n      {:phoenix_live_view, \"~&gt; 0.15.4\", override: true},\n      {:timex, \"~&gt; 3.6\"},\n      {:faker, \"~&gt; 0.16.0\"}\n    ]\n  end\n</pre><p><br></p><p>We updated :phoenix_live_view to 15.4 version and added timex to handle times and faker for when we want test data.</p><h2>Set Up TailwindCSS And AlpineJS</h2><p>Make sure to have the latest node and npm versions.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ cd assets</code></p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ npm i tailwindcss postcss autoprefixer postcss-loader@4.2 --save-dev</code></p><p>Next let's configure Webpack, PostCSS, and TailwindCSS.</p><pre class=\"ql-syntax\" spellcheck=\"false\">// /assets/webpack.config.js\n\nuse: [\n  MiniCssExtractPlugin.loader,\n  'css-loader',\n  'sass-loader',\n  'postcss-loader', // Add this\n],\n</pre><p><br></p><p>Add&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/assets/postcss.config.js</code>&nbsp;file with the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">// /assets/postcss.config.js\n\nmodule.exports = {\n    plugins: {\n        \"postcss-import\": {},\n        tailwindcss: {},\n        autoprefixer: {}\n    }\n}\n</pre><p><br></p><p>Create a TailwindCSS configuration file.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ npx tailwindcss init</code></p><p>Add the following configuration to that file:</p><pre class=\"ql-syntax\" spellcheck=\"false\">const colors = require('tailwindcss/colors')\n\nmodule.exports = {\n  purge: {\n    enabled: process.env.NODE_ENV === \"production\",\n    content: [\n      \"../lib/**/*.eex\",\n      \"../lib/**/*.leex\",\n      \"../lib/**/*_view.ex\"\n    ],\n    options: {\n      whitelist: [/phx/, /nprogress/]\n    }\n  },\n  theme: {\n    extend: {\n      colors: {\n        'light-blue': colors.lightBlue,\n        cyan: colors.cyan,\n      },\n    },\n  },\n  variants: {\n    extend: {\n      borderWidth: ['hover'],\n    }\n  },\n  plugins: [require('@tailwindcss/forms')],\n}\n</pre><p><br></p><p>We configure which files to purge, added a custom color, and custom forms plugin. So let's add custom forms to our npm dependencies now.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ npm i @tailwindcss/forms --save-dev</code></p><p>For custom components conflicts let's add postcss-import plugin.</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ npm i postcss-import --save-dev</code></p><p>Go to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/assets/css/app.scss</code>&nbsp;and add the following at the top of the file:</p><pre class=\"ql-syntax\" spellcheck=\"false\">/* This file is for your main application css. */\n@import \"tailwindcss/base\";\n@import \"tailwindcss/components\";\n@import \"tailwindcss/utilities\";\n</pre><p><br></p><p>Delete&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/assets/css/phoenix.css</code>&nbsp;we won't need it.</p><p>Let's get out of our assets folder&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ cd ..</code>&nbsp;and run our server&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ iex -S mix phx.server</code></p><p>Test it out buy going to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.html.leex</code>&nbsp;delete everything and add the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;h1 class=\"text-red-500 text-5xl font-bold text-center\"&gt;Instagram Clone&lt;/h1&gt;\n</pre><p><br></p><p>We should have a big red headline on our homepage.</p><p>Go to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.ex</code>&nbsp;delete everything because we won't need any of that in our homepage, and add the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">defmodule InstagramCloneWeb.PageLive do\n  use InstagramCloneWeb, :live_view\n\n  @impl true\n  def mount(_params, _session, socket) do\n    {:ok, socket}\n  end\nend\n</pre><p><br></p><p>Go to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/templates/layout/root.html.leex</code>&nbsp;delete the default phoenix header, you should have the following on that file:</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;!DOCTYPE html&gt;\n&lt;html lang=\"en\"&gt;\n  &lt;head&gt;\n    &lt;meta charset=\"utf-8\"/&gt;\n    &lt;meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"/&gt;\n    &lt;meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/&gt;\n    &lt;%= csrf_meta_tag() %&gt;\n    &lt;%= live_title_tag assigns[:page_title] || \"InstagramClone\", suffix: \" · Phoenix Framework\" %&gt;\n    &lt;link phx-track-static rel=\"stylesheet\" href=\"&lt;%= Routes.static_path(@conn, \"/css/app.css\") %&gt;\"/&gt;\n    &lt;script defer phx-track-static type=\"text/javascript\" src=\"&lt;%= Routes.static_path(@conn, \"/js/app.js\") %&gt;\"&gt;&lt;/script&gt;\n  &lt;/head&gt;\n  &lt;body&gt;\n    &lt;!-- Remove Everything Above Here --&gt;\n    &lt;%= @inner_content %&gt;\n  &lt;/body&gt;\n&lt;/html&gt;\n</pre><p><br></p><p>Now let's customize our main container with tailwind, go to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/templates/layout/live.html.leex</code>&nbsp;and add the following class to the main tag:</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;main role=\"main\" class=\"container mx-auto max-w-full md:w-11/12 2xl:w-6/12 pt-24\"&gt; &lt;!-- This the class that we added --&gt;\n  &lt;p class=\"alert alert-info\" role=\"alert\"\n    phx-click=\"lv:clear-flash\"\n    phx-value-key=\"info\"&gt;&lt;%= live_flash(@flash, :info) %&gt;&lt;/p&gt;\n\n  &lt;p class=\"alert alert-danger\" role=\"alert\"\n    phx-click=\"lv:clear-flash\"\n    phx-value-key=\"error\"&gt;&lt;%= live_flash(@flash, :error) %&gt;&lt;/p&gt;\n\n  &lt;%= @inner_content %&gt;\n&lt;/main&gt;\n</pre><p><br></p><p>&nbsp;</p><h3>Add AlpineJS</h3><p>With TailwindCSS ready to go let's add AlpineJS. Let's get into our&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ cd assets</code>&nbsp;folder again and run the following:</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ npm i alpinejs</code></p><p>Open the app.js file located&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/assets/js/app.js</code>&nbsp;and add the following so that we don't have any conflict with LiveView's own DOM patching:</p><pre class=\"ql-syntax\" spellcheck=\"false\">import Alpine from \"alpinejs\"\n\nlet csrfToken = document.querySelector(\"meta[name='csrf-token']\").getAttribute(\"content\")\nlet liveSocket = new LiveSocket(\"/live\", Socket, {\n  params: { _csrf_token: csrfToken },\n  dom: {\n    onBeforeElUpdated(from, to) {\n      if (from.__x) { Alpine.clone(from.__x, to) }\n    }\n  }\n})\n</pre><p><br></p><p>Let's get out of our assets folder&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ cd ..</code>&nbsp;and run our server&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ iex -S mix phx.server</code></p><p>Test it out buy going to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.html.leex</code>&nbsp;and adding the following to our top of our file:</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;div x-data=\"{ open: false }\"&gt;\n    &lt;button @click=\"open = true\"&gt;Open Dropdown&lt;/button&gt;\n\n    &lt;ul\n        x-show=\"open\"\n        @click.away=\"open = false\"\n    &gt;\n        Dropdown Body\n    &lt;/ul&gt;\n&lt;/div&gt;\n</pre><p><br></p><p>We should have a clickable dropdown if we go to our homepage like the example below:</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--lQ0_y-SX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4w2rzfnpz3ms1qov0aco.gif\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--lQ0_y-SX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4w2rzfnpz3ms1qov0aco.gif\" alt=\"AlpineJS Test\"></a></p><p>&nbsp;</p><h2>Phx.Gen.Auth</h2><p>With that set up out of the way the real fun begins. Let's add user authentication with phx.gen.auth package.</p><p>Let's add the package to our&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">mix.exs</code>&nbsp;file.</p><pre class=\"ql-syntax\" spellcheck=\"false\">  defp deps do\n    [\n      {:phoenix, \"~&gt; 1.5.6\"},\n      {:phoenix_ecto, \"~&gt; 4.1\"},\n      {:ecto_sql, \"~&gt; 3.4\"},\n      {:postgrex, \"&gt;= 0.0.0\"},\n      {:floki, \"&gt;= 0.27.0\", only: :test},\n      {:phoenix_html, \"~&gt; 2.11\"},\n      {:phoenix_live_reload, \"~&gt; 1.2\", only: :dev},\n      {:phoenix_live_dashboard, \"~&gt; 0.3 or ~&gt; 0.2.9\"},\n      {:telemetry_metrics, \"~&gt; 0.4\"},\n      {:telemetry_poller, \"~&gt; 0.4\"},\n      {:gettext, \"~&gt; 0.11\"},\n      {:jason, \"~&gt; 1.0\"},\n      {:plug_cowboy, \"~&gt; 2.0\"},\n      {:phoenix_live_view, \"~&gt; 0.15.4\", override: true},\n      {:timex, \"~&gt; 3.6\"},\n      {:faker, \"~&gt; 0.16.0\"},\n      {:phx_gen_auth, \"~&gt; 0.7\", only: [:dev], runtime: false}\n    ]\n  end\n</pre><p><br></p><p>Install and compile the dependencies</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ mix do deps.get, deps.compile</code></p><p>Install the authentication system with the following command:</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ mix phx.gen.auth Accounts User users</code></p><p>After all the files were generated run the following command:</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ mix deps.get &amp;&amp; mix ecto.migrate</code></p><p>Now we need to add some fields to our users table by running the following command:</p><p><code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ mix ecto.gen.migration add_to_users_table</code></p><p>Then open the file that was generated&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">priv/repo/migrations/20210409223611_add_to_users_table.exs</code>&nbsp;and add the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">defmodule InstagramClone.Repo.Migrations.AddToUsersTable do\n  use Ecto.Migration\n\n  def change do\n    alter table(:users) do\n      add :username, :string\n      add :full_name, :string\n      add :avatar_url, :string\n      add :bio, :string\n      add :website, :string\n    end\n  end\nend\n</pre><p><br></p><p>Then&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ mix ecto.migrate</code></p><p>Next open&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">lib/instagram_clone/accounts/user.ex</code>&nbsp;and add the following to your users schema:</p><pre class=\"ql-syntax\" spellcheck=\"false\">field :username, :string\nfield :full_name, :string\nfield :avatar_url, :string, default: \"/images/default-avatar.png\"\nfield :bio, :string\nfield :website, :string\n</pre><p><br></p><p>&nbsp;</p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--GlyR_nSb--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ogf5i7oq4wd4muyncv9u.png\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--GlyR_nSb--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ogf5i7oq4wd4muyncv9u.png\" alt=\"default-avatar\"></a></p><p>&nbsp;</p><p>Download the default avatar image above and rename it to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">default-avatar.png</code>&nbsp;and add that image to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">priv/static/images</code></p><p>Now we need to add validations for our new users schema, so open&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">lib/instagram_clone/accounts/user.ex</code>&nbsp;again and change the&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">registration_changeset</code>&nbsp;to the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">  def registration_changeset(user, attrs, opts \\\\ []) do\n    user\n    |&gt; cast(attrs, [:email, :password, :username, :full_name, :avatar_url, :bio, :website])\n    |&gt; validate_required([:username, :full_name])\n    |&gt; validate_length(:username, min: 5, max: 30)\n    |&gt; validate_format(:username, ~r/^[a-zA-Z0-9_.-]*$/, message: \"Please use letters and numbers without space(only characters allowed _ . -)\")\n    |&gt; unique_constraint(:username)\n    |&gt; validate_length(:full_name, min: 4, max: 30)\n    |&gt; validate_email()\n    |&gt; validate_password(opts)\n  end\n</pre><p><br></p><p>Also, we need to change our&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">validate_password</code>&nbsp;function for when we update the user's account, we won't need to validate or hash the password so change it to the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">  defp validate_password(changeset, opts) do\n    register_user? = Keyword.get(opts, :register_user, true)\n    if register_user? do\n      changeset\n      |&gt; validate_required([:password])\n      |&gt; validate_length(:password, min: 6, max: 80)\n      # |&gt; validate_format(:password, ~r/[a-z]/, message: \"at least one lower case character\")\n      # |&gt; validate_format(:password, ~r/[A-Z]/, message: \"at least one upper case character\")\n      # |&gt; validate_format(:password, ~r/[!?@#$%^&amp;*_0-9]/, message: \"at least one digit or punctuation character\")\n      |&gt; maybe_hash_password(opts)\n    else\n      changeset\n    end\n  end\n</pre><p><br></p><p>When updating the user's account we will send a&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">register_user: false</code>&nbsp;option to the changeset. Also, the minimum password length was changed to 6 for development purposes only it should be changed in production.</p><p>Let's run our server&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">$ iex -S mix phx.server</code>&nbsp;and open&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.html.leex</code>&nbsp;to work on our homepage styles to add the registration form.</p><p>Before we do that we have to delete the authentication links auto generated by phx.gen.auth so go to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/templates/layout/root.html.leex</code>&nbsp;and delete the&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">&lt;%= render \"_user_menu.html\", assigns %&gt;</code>&nbsp;from the top of the body.</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;!DOCTYPE html&gt;\n&lt;html lang=\"en\"&gt;\n  &lt;head&gt;\n    &lt;meta charset=\"utf-8\"/&gt;\n    &lt;meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"/&gt;\n    &lt;meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/&gt;\n    &lt;%= csrf_meta_tag() %&gt;\n    &lt;%= live_title_tag assigns[:page_title] || \"InstagramClone\", suffix: \" · Phoenix Framework\" %&gt;\n    &lt;link phx-track-static rel=\"stylesheet\" href=\"&lt;%= Routes.static_path(@conn, \"/css/app.css\") %&gt;\"/&gt;\n    &lt;script defer phx-track-static type=\"text/javascript\" src=\"&lt;%= Routes.static_path(@conn, \"/js/app.js\") %&gt;\"&gt;&lt;/script&gt;\n  &lt;/head&gt;\n  &lt;body&gt;\n    &lt;%= render \"_user_menu.html\", assigns %&gt;&lt;!-- REMOVE IT --&gt;\n    &lt;%= @inner_content %&gt;\n  &lt;/body&gt;\n&lt;/html&gt;\n</pre><p><br></p><p>And lastly, delete&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/templates/layout/_user_menu.html.eex</code>&nbsp;partial file, we won't need it.</p><p>Okay now back to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.html.leex</code>&nbsp;add the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;section class=\"w-1/2 border-2 shadow-lg flex flex-col place-items-center mx-auto p-6\"&gt;\n    &lt;h1 class=\"text-4xl font-bold italic text-gray-600\"&gt;InstagramClone&lt;/h1&gt;\n    &lt;p class=\"text-gray-400 font-semibold text-lg my-6\"&gt;Sign up to see photos and videos from your friends.&lt;/p&gt;\n&lt;/section&gt;\n</pre><p><br></p><p>We need to add a form so go to&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.ex</code>&nbsp;change the mount function to the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">  alias InstagramClone.Accounts\n  alias InstagramClone.Accounts.User\n\n  @impl true\n  def mount(_params, _session, socket) do\n    changeset = Accounts.change_user_registration(%User{})\n    {:ok,\n      socket\n      |&gt; assign(changeset: changeset)}\n  end\n</pre><p><br></p><p>Let's add our form and new styles by editing&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">/lib/instagram_clone_web/live/page_live.html.leex</code>&nbsp;to:</p><pre class=\"ql-syntax\" spellcheck=\"false\">&lt;section class=\"w-1/2 border-2 shadow flex flex-col place-items-center mx-auto p-6\"&gt;\n  &lt;h1 class=\"text-4xl font-bold italic text-gray-700\"&gt;InstagramClone&lt;/h1&gt;\n  &lt;p class=\"text-gray-500 font-semibold text-lg mt-6 text-center px-8\"&gt;Sign up to see photos and videos from your friends.&lt;/p&gt;\n\n  &lt;%= f = form_for @changeset, \"#\",\n    phx_change: \"validate\",\n    phx_submit: \"save\",\n    phx_trigger_action: @trigger_submit,\n    class: \"flex flex-col space-y-4 w-full px-6\" %&gt;\n\n    &lt;div class=\"flex flex-col\"&gt;\n      &lt;%= label f, :email, class: \"text-gray-400\" %&gt;\n      &lt;%= email_input f, :email, class: \"rounded border-gray-300 shadow-sm focus:ring-gray-900 focus:ring-opacity-50 focus:border-gray-900\" %&gt;\n      &lt;%= error_tag f, :email, class: \"text-red-700 text-sm\" %&gt;\n    &lt;/div&gt;\n\n    &lt;div class=\"flex flex-col\"&gt;\n      &lt;%= label f, :full_name, class: \"text-gray-400\" %&gt;\n      &lt;%= text_input f, :full_name, class: \"rounded border-gray-300 shadow-sm focus:ring-gray-900 focus:ring-opacity-50 focus:border-gray-900\" %&gt;\n      &lt;%= error_tag f, :full_name, class: \"text-red-700 text-sm\" %&gt;\n    &lt;/div&gt;\n\n    &lt;div class=\"flex flex-col\"&gt;\n      &lt;%= label f, :username, class: \"text-gray-400\" %&gt;\n      &lt;%= text_input f, :username, class: \"rounded border-gray-300 shadow-sm focus:ring-gray-900 focus:ring-opacity-50 focus:border-gray-900\" %&gt;\n      &lt;%= error_tag f, :username, class: \"text-red-700 text-sm\" %&gt;\n    &lt;/div&gt;\n\n    &lt;div class=\"flex flex-col\"&gt;\n      &lt;%= label f, :password, class: \"text-gray-400\" %&gt;\n      &lt;%= password_input f, :password, class: \"rounded border-gray-300 shadow-sm focus:ring-gray-900 focus:ring-opacity-50 focus:border-gray-900\" %&gt;\n      &lt;%= error_tag f, :password, class: \"text-red-700 text-sm\" %&gt;\n    &lt;/div&gt;\n\n    &lt;div&gt;\n      &lt;%= submit \"Sign up\", phx_disable_with: \"Saving...\", class: \"block w-full py-2 border-none shadow rounded font-semibold text-sm text-gray-50 hover:bg-light-blue-600 bg-light-blue-500 cursor-pointer\" %&gt;\n    &lt;/div&gt;\n\n  &lt;/form&gt;\n\n  &lt;p class=\"text-sm px-10 text-center mt-6 text-gray-400 font-semibold\"&gt;By signing up, you agree to our Terms , Data Policy and Cookies Policy .&lt;/p&gt;\n&lt;/section&gt;\n\n&lt;section class=\"w-1/2 border-2 shadow flex justify-center mx-auto p-6 mt-6\"&gt;\n  &lt;p class=\"text-lg text-gray-600\"&gt;Have an account? &lt;%= link \"Log in\", to: Routes.user_session_path(@socket, :new), class: \"text-light-blue-500 font-semibold\" %&gt;&lt;/p&gt;\n&lt;/section&gt;\n</pre><p><br></p><p>We need to tweak a little bit our&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">error_tag()</code>&nbsp;helper functions before we go further, so we can add classes to it, open&nbsp;<code style=\"color: var(--color-body-color); background-color: rgba(0, 0, 0, 0.1);\">lib/instagram_clone_web/views/error_helpers.ex</code>&nbsp;file and change the function to the following:</p><pre class=\"ql-syntax\" spellcheck=\"false\">  def error_tag(form, field, class \\\\ [class: \"invalid-feedback\"]) do\n    Enum.map(Keyword.get_values(form.errors, field), fn error -&gt;\n      content_tag(:span, translate_error(error),\n        class: Keyword.get(class, :class),\n        phx_feedback_for: input_id(form, field)\n      )\n    end)\n  end\n</pre><p><br></p><p><a href=\"https://res.cloudinary.com/practicaldev/image/fetch/s--ePCJxnX0--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/iu4hwmlpqnhegvsl4b8x.jpg\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--ePCJxnX0--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/iu4hwmlpqnhegvsl4b8x.jpg\" alt=\"InstagramCloneHomepage\"></a></p>''',
                title='Let\'s Build An Instagram Clone With The PETAL(Phoenix, Elixir, TailwindCSS, AlpineJS, LiveView) Stack',
                coding_languages=[
                    "JS",
                    "HTML"
                ],
                languages=['ENG'],
                categories=['FE', 'BE', 'UI'],
                user=ep2,
                is_published=True,
            )
            a.thumbnail.save('article5.jpg', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article5.jpg', 'rb')))
            a.save()

            a = Article(
                content='''<p>Whether you are a beginner or an experienced developer, quality IDEs or code editors are useful. With them, you don't need to spend a lot of time setting up tools, and they help optimize development. In addition, constant updates help developers keep track of innovations. Let's go through the well-known IDE and code editor for Python and analyze their pros and cons.</p><h1>PyCharm</h1><p>Cross-platform IDE is compatible with&nbsp;<strong>Linux</strong>,&nbsp;<strong>macOS</strong>, and&nbsp;<strong>Windows</strong>. Supports Python versions 2 (2.7) and Python 3 (3.5 and higher). It comes with testing and debugging support, refactoring features, and code navigation. It also allows you to run, debug, test, and deploy applications on remote hosts or virtual machines.</p><p>The professional edition allows you to use popular frameworks and libraries for Data Science. The code editor supports&nbsp;<strong>JavaScript</strong>,&nbsp;<strong>TypeScript</strong>,&nbsp;<strong>CoffeeScript</strong>,&nbsp;<strong>JS</strong>, and&nbsp;<strong>Node.js</strong>,&nbsp;<strong>AngularJS</strong>, and more.</p><p><a href=\"https://www.jetbrains.com/pycharm/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">PyCharm</a>&nbsp;can be integrated with VCS and database tools; remote interpreters, SSH clients, Vagrant and Docker, Oracle, PostgreSQL, MySQL, and SQL Server. It also supports IPython Notebook, Anaconda, and so on.</p><h2>Pros:</h2><ul><li>the ability to view the entire source code with a single click;</li><li>lots of plugins;</li><li>easy to use;</li><li>great community support;</li><li>easy installation.</li></ul><h2>Cons:</h2><ul><li>some chips are only available in the paid version;</li><li>there may be a problem when trying to fix tools like venv;</li><li>resource-intensive.</li></ul><h1>Sublime Text</h1><p><a href=\"https://www.sublimetext.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Sublime Text</a>&nbsp;is a cross-platform text editor in C++ and Python. Originally developed&nbsp;<strong>as an extension for Vim</strong>. Since version 2.0, it supports&nbsp;<strong>44 major programming languages</strong>, including Python. Its main principles: a minimalistic interface and an emphasis on code.</p><p>It is a fast text editor for organizing code. It is easy to configure, has high performance and a powerful API. In addition, it is convenient to switch between projects, search for specific fragments in the code and go to any function or symbol.</p><h2>Pros:</h2><ul><li>high performance;</li><li>simple interface;</li><li>supports many languages.</li></ul><h2>Cons:</h2><ul><li>no debugger;</li><li>it may be difficult for beginners;</li><li>you need a license.</li></ul><h1>Visual Studio Code</h1><p><a href=\"https://code.visualstudio.com/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Visual Studio Code</a>&nbsp;is an open-source cross-platform code editor from Microsoft. Inside, there is a debugger, an IntelliSense&nbsp;<strong>code auto-completion mechanism</strong>, Lint support, and integration with version control systems. As well as a built-in terminal and a large market of free extensions and the ability to work with the frameworks nunit mstest, pytest or nose.</p><p>For fans of a minimalistic interface, there is a \"zen mode\". It only shows the file you are currently working on and hides the \"extra\" interface.</p><p>VS Code is a&nbsp;<strong>lightweight IDE</strong>&nbsp;that can be extended with a variety of plugins. It also adds support for new languages, themes, debugger, and so on.</p><h2>Pros:</h2><ul><li>almost five thousand extensions;</li><li>import keyboard shortcuts from other code editors;</li><li>easy;</li><li>user-friendly interface.</li></ul><h2>Cons:</h2><ul><li>slow startup;</li><li>slow search;</li><li>performance is reduced if you install a lot of plugins.</li></ul><h1>Atom</h1><p>An open-source cross-platform editor written in CSS, JavaScript, HTML, and Node.js.</p><p><a href=\"https://atom.io/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Atom</a>&nbsp;comes with a built-in package manager where you can download and install additional packages. And also create your own. A large community is working on creating new packages.</p><p>Atom has&nbsp;<strong>Git and GitHub integration</strong>, and the ability to work on code together with colleagues in real-time using Teletype.</p><p>The editor has a clean and fully customizable user interface, with 8 light and dark themes pre-installed.&nbsp;<strong>You can configure everything</strong>, right down to the basic functions.</p><h2>Pros:</h2><ul><li>fully customizable interface;</li><li>built-in package manager;</li><li>great community support.</li></ul><h2>Cons:</h2><ul><li>takes up a lot of RAM;</li><li>need optimization;</li><li>the performance is lower than that of some competitors (for example, Sublime Text).</li></ul><h1>Thonny</h1><p><a href=\"https://thonny.org/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Thonny</a>&nbsp;is a free Python IDE designed specifically&nbsp;<strong>for beginners</strong>. Comes with a built-in version of Python v3. x. Compatible with Linux, macOS, and Windows.</p><p>The built-in debugger makes it easy to find syntax errors, such as parentheses and unclosed quotes. In addition, it is easy to use, and you do not need to know the breakpoints.</p><p>Variables are represented based on a simplified model (but you can also switch to realistic ones). It also has a simple package installation interface and a record of user actions. It is useful to analyze the work at first.</p><h2>Pros:</h2><ul><li>simple interface;</li><li>suitable for beginners;</li><li>no distractions.</li></ul><h2>Cons:</h2><ul><li>the basic functionality may not be enough to work with.</li></ul><h1>Spyder</h1><p>An IDE designed for data analysts and engineers and compatible with Linux, macOS, and Windows.</p><p><a href=\"https://www.spyder-ide.org/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Spyder</a>&nbsp;uses a PDB debugger that displays the line, file, and state of each breakpoint. And can quickly edit variables at each point through the variable explorer. By the way, the explorer itself shows links to all objects and allows you to interact with them.</p><p>The IDE comes with a large library that is loaded when installed with Anaconda. You can also download&nbsp;<strong>more than 1,500 additional Python or R data science packages</strong>. Spyder also allows you to extend the functionality with third-party plugins, such as Spyder Notebook, Terminal, UnitTest, Reports, and so on.</p><h2>Pros:</h2><ul><li>fairly light and fast;</li><li>easy to learn, suitable for beginners;</li><li>suitable for research work.</li></ul><h2>Cons:</h2><ul><li>difficulties with the integration of version control systems;</li><li>it is difficult to configure.</li></ul><h1>Pyzo</h1><p>An open-source cross-platform IDE for Python that strives for simplicity and interactivity.</p><p>The system is based on two components:&nbsp;<strong>the shell and the tools</strong>. These include the source structure, online help, workspace, project manager, and so on. The code for&nbsp;<a href=\"https://pyzo.org/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Pyzo</a>&nbsp;is written in Python 3 with a Qt GUI.</p><p>The shell includes magic commands, creating multiple configurations, pip support for package management, PySide, Tk, PyQt4, GTK, fltk, and wx, post-mortem debugging, and more.</p><h2>Pros:</h2><ul><li>simple;</li><li>good support for beginners.</li></ul><h2>Cons:</h2><ul><li>you need a distribution.</li></ul><h1>Eric Python IDE</h1><p>This is a cross-platform IDE written in Python.&nbsp;<a href=\"https://eric-ide.python-projects.org/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">Eric</a>&nbsp;has a powerful debugger that debugs multithreaded and multiprocessor programs. There is support for&nbsp;<strong>unit testing</strong>, a built-in hex editor, an SQL browser, an icon designer, and many other tools. Thanks to the built-in Qt supports the creation of&nbsp;<strong>graphical interfaces</strong>&nbsp;using Qt Designer.</p><p>The IDE has an advanced project management system, an automatic code completion feature, and the ability to collaborate in real-time. Eric supports Mercurial and SVN version control. Git support is available through the plugin.</p><h2>Pros</h2><ul><li>suitable for complex projects;</li><li>spell check;</li><li>the ability to work with other developers in real-time.</li></ul><h2>Cons:</h2><ul><li>overloaded interface;</li><li>it can be difficult to install.</li></ul><h1>Vim</h1><p>Cross-platform modal code editor for Python. Supports three operating modes: normal, insert mode, and command-line mode.</p><p>Vim is free software that supports many plugins and extensions and works with different programming languages. It is configured by adding extensions or changing its configuration file. So, it is easy to adapt it for Python development.</p><p>It also supports non-software applications that other editors don't have.</p><h2>Pros:</h2><ul><li>recognition and conversion of file formats (UNIX, MS-DOS or Mac);</li><li>lots of plugins;</li><li>you can configure and extend it with .vimrc.</li></ul><h2>Cons:</h2><ul><li>it takes time to master;</li><li>not the most user-friendly interface.</li></ul><p><strong>Hope you enjoyed my article. Follow my&nbsp;</strong><a href=\"https://github.com/ra1nbow1\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><strong>Github</strong></a><strong>&nbsp;&lt;3</strong></p>''',
                title='Python IDEs and code editors compilation',
                coding_languages=[
                    "PY",
                ],
                languages=['ENG'],
                categories=[
                    "SEC",
                    "DB",
                    "FE",
                    "BE",
                    "ML"
                ],
                user=ep1,
                is_published=True,
            )
            a.thumbnail.save('article6.jpg', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article6.jpg', 'rb')))
            a.save()

            a = Article(
                content='''<h2>Long story short</h2><p>The glassmorphim effect is one of the trends that began in 2020, which also stays with us in 2021. Although this effect is not really as new in web design as it might seem, more about it later in this article. The \"frosted glass\" effect, which is most often used in the visualization of credit cards, has won the hearts of many designers and has mastered sites like Dribbble. We have pastel versions, in vivid colors or dark mode, lots of possibilities. However, today I would like to show you how to use this great effect in your website design, for example, a landing page or portfolio. Let's get down to business.</p><h2>Where did it come from</h2><p>As I mentioned in the introduction, blurry backgrounds have already been used in the Windows Vista UI, for example in the menu that opens when you click \"start\". It was a black transparent background. In 2013, Apple introduced this effect in iOS 7, which was visible, including when swiping upwards on the screen. Currently, Microsoft uses this effect, called The Acrylic, in its design language, Fluent Design System. I think that's enough history, so let's move on to the modern guidelines necessary to create a glassmorphim effect in a web project.</p><h2>What are the rules of that trend</h2><p>Characteristic for glassmorphism are:</p><ul><li>It imitates the look of the frosted glass by using background blur</li><li>The see-through concept</li><li>Hierarchy and structure of the layers</li><li>Use clear shapes and vivid colors in the background to emphasize the blurred transparency</li><li>Translucent objects have a subtle border</li></ul><h2>How to achieve this effect with CSS</h2><p>Achieving this effect is very simple with the MDB generator you can find&nbsp;<a href=\"https://mdbootstrap.com/docs/standard/tools/design/masks/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">here</a>. Just use the sliders to choose the \"blur\" and \"transparency\" values and choose a background color, and the tool will generate the necessary CSS and HTML code. Then you add the generated code to your project and voila! A beautiful, subtle glassmorphism effect already appears on your website. To make it even easier and more pleasant for you, I have prepared three projects in which I show you various possibilities of its use.</p><h2>Project 1 - simple intro page</h2><p>In this&nbsp;<a href=\"https://mdbootstrap.com/snippets/standard/marta-szymanska/2868059\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">project</a>, I use the glassmorphim effect on the background as a mask that blurs the photo in vivid colors and highlights the most important text in the center of the intro.</p><p><a href=\"https://mdbootstrap.com/snippets/standard/marta-szymanska/2868059\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--9CWVGkd5--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://mdbcdn.b-cdn.net/img/Photos/new-templates/glassmorphism-article/img12.png\" alt=\"image1\"></a></p><h2>Project 2 - intro page with a card</h2><p>In this&nbsp;<a href=\"https://mdbootstrap.com/snippets/standard/marta-szymanska/2868061\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">project</a>, I created a glassmorphism card, where I added a few additional styles to the basic styles from the generator, such as border, border-radius, background-clip, etc., and attached&nbsp;<a href=\"https://mdbootstrap.com/docs/standard/content-styles/animations/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">MDB animations</a>&nbsp;to get an even better visual effect.</p><p><a href=\"https://mdbootstrap.com/docs/standard/content-styles/animations/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--SdEcxutC--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://mdbcdn.b-cdn.net/img/Photos/new-templates/glassmorphism-article/img11.png\" alt=\"image2\"></a></p><h2>Project 3 - personal cards</h2><p>In this&nbsp;<a href=\"https://mdbootstrap.com/snippets/standard/marta-szymanska/2868064\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">project</a>, I created a set of cards that you can use, for example, to represent your team or your customers' opinions. Instead of the white translucent background of the card, I used a dark gray so that you could use the glassmorphism effect in a dark mode as well, and also added more delicate animations.</p><p><a href=\"https://mdbootstrap.com/snippets/standard/marta-szymanska/2868064\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\"><img src=\"https://res.cloudinary.com/practicaldev/image/fetch/s--1xaj7mAR--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://mdbcdn.b-cdn.net/img/Photos/new-templates/glassmorphism-article/img13.png\" alt=\"image3\"></a></p><h2>Summary</h2><p>Hopefully, the examples above will convince you that glassmorphism is a trend that is easy to achieve with CSS, yet has a wow effect. It is definitely useful when you want to highlight important content and spoils for a minimalist style. Of course, it is not worth overusing it, and I believe that one or two sections on the site will be enough. Try, experiment, and share your projects in&nbsp;<a href=\"https://mdbootstrap.com/snippets/\" rel=\"noopener noreferrer\" target=\"_blank\" style=\"color: var(--accent-brand);\">MDB snippets</a>. Good luck!</p>''',
                title='Using the glassmorphism UI trend in your web project',
                coding_languages=[
                    "JS",
                    "HTML",
                    "CSS"
                ],
                languages=['ENG'],
                categories=[
                    "FE",
                    "UI"
                ],
                user=ep1,
                is_published=True,
            )
            a.thumbnail.save('article7.jpg', ImageFile(open('./codeine_django/common/management/demo_assets/articles/article7.jpg', 'rb')))
            a.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Articles created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            # initiate some code reviews
            self.stdout.write('Initiating some code reviews...')
            now = timezone.now()
            u1 = BaseUser.objects.get(email='m1@m1.com')

            cr = CodeReview(
                title="Random Questions Subset Algo",
                code="class QuizSerializer(serializers.ModelSerializer):\r\n    question_groups = QuestionGroupSerializer(many=True)\r\n    questions = serializers.SerializerMethodField('get_questions')\r\n\r\n    class Meta:\r\n        model = Quiz\r\n        fields = ('id', 'passing_marks', 'course', 'course_material', 'instructions', 'is_randomized', 'question_groups', 'questions')\r\n    # end Meta\r\n\r\n    def get_questions(self, obj):\r\n        request = self.context.get('request')\r\n        try:\r\n            member = request.user.member\r\n            random.seed(int(member.id))\r\n            questions = []\r\n\r\n            for question_group in obj.question_groups.all():\r\n                tmp = random.sample(list(question_group.question_bank.questions.all()), k=question_group.count)\r\n                questions += tmp\r\n            # end for\r\n            return QuestionSerializer(questions, many=True, context=self.context).data\r\n        except Exception as e:\r\n            try:\r\n                partner = request.user.partner\r\n                questions = []\r\n\r\n                for question_group in obj.question_groups.all():\r\n                    questions += question_group.question_bank.questions.all()\r\n                # end for\r\n                return QuestionSerializer(questions, many=True, context=self.context).data\r\n            except Exception as e:\r\n                print(str(e))\r\n                return []\r\n        # end try-except\r\n    # end def\r\n# end class",
                coding_languages=['PY'],
                languages=['ENG'],
                categories=['BE'],
                user=u1,
                timestamp=now - timedelta(hours=2)
            )
            cr.save()

            cr_c1 = CodeReviewComment(
                comment="<p>What is this serializer for?</p>",
                user=u1,
                code_review=cr,
                parent_comment=None,
                code_line_index=1,
            )
            cr_c1.save()

            cr_c2 = CodeReviewComment(
                comment="<p>This serializes the quiz and a random subset of questions for each quiz</p>",
                user=u,
                code_review=cr,
                parent_comment=cr_c1,
                code_line_index=1,
            )
            cr_c2.save()

            u2 = BaseUser.objects.get(email='m2@m2.com')

            cr = CodeReview(
                title="JS Date Formatter",
                code="export const calculateDateInterval = (timestamp) => {\r\n  const dateBefore = new Date(timestamp);\r\n  const dateNow = new Date();\r\n\r\n  let seconds = Math.floor((dateNow - dateBefore) / 1000);\r\n  let minutes = Math.floor(seconds / 60);\r\n  let hours = Math.floor(minutes / 60);\r\n  let days = Math.floor(hours / 24);\r\n\r\n  hours = hours - days * 24;\r\n  minutes = minutes - days * 24 * 60 - hours * 60;\r\n  seconds = seconds - days * 24 * 60 * 60 - hours * 60 * 60 - minutes * 60;\r\n\r\n  if (days === 0) {\r\n    if (hours === 0) {\r\n      if (minutes === 0) {\r\n        return `${seconds} seconds ago`;\r\n      }\r\n\r\n      if (minutes === 1) {\r\n        return `${minutes} minute ago`;\r\n      }\r\n      return `${minutes} minutes ago`;\r\n    }\r\n\r\n    if (hours === 1) {\r\n      return `${hours} hour ago`;\r\n    }\r\n    return `${hours} hours ago`;\r\n  }\r\n\r\n  if (days === 1) {\r\n    return `${days} day ago`;\r\n  }\r\n  return `${days} days ago`;\r\n};",
                coding_languages=['JS'],
                languages=['ENG'],
                categories=['FE'],
                user=u2,
                timestamp=now - timedelta(hours=2)
            )
            cr.save()

            cr_c1 = CodeReviewComment(
                comment="<p>Looking for improvements...</p>",
                user=u2,
                code_review=cr,
                parent_comment=None,
                code_line_index=1,
            )
            cr_c1.save()

            cr_c2 = CodeReviewComment(
                comment="<p>Use typescript fag</p>",
                user=u1,
                code_review=cr,
                parent_comment=cr_c1,
                code_line_index=1,
            )
            cr_c2.save()

            cr_c3 = CodeReviewComment(
                comment="<p>Don't be rude, son</p>",
                user=u,
                code_review=cr,
                parent_comment=cr_c2,
                code_line_index=1,
            )
            cr_c3.save()

            article = Article.objects.get(title='8 JavaScript Tips & Tricks That No One Teaches 🚀')

            cr_c3 = CodeReviewComment(
                comment=f'<p>Check out an <a href=\"http://localhost:3000/article/{article.id}\" rel=\"noopener noreferrer\" target=\"_blank\">article</a> I wrote!</p>',
                user=u,
                code_review=cr,
                parent_comment=cr_c2,
                code_line_index=1,
            )
            cr_c3.save()

            cr_c1 = CodeReviewComment(
                comment="<p>3 nested ifs....</p>",
                user=u,
                code_review=cr,
                parent_comment=None,
                code_line_index=14,
            )
            cr_c1.save()

            cr = CodeReview(
                title="Buffer Overflow Attack",
                code="#include <signal.h>\r\n#include <stdio.h>\r\n#include <string.h>\r\nint main(){\r\n\tchar realPassword[20];\r\n\tchar givenPassword[20];\r\n\r\n\tstrncpy(realPassword, \"ddddddddddddddd\", 20);\r\n\tgets(givenPassword);\r\n\t\r\n\tif (0 == strncmp(givenPassword, realPassword, 20)){\r\n\t\tprintf(\"SUCCESS!\\n\");\r\n\t}else{\r\n\t\tprintf(\"FAILURE!\\n\");\r\n\t}\r\n\traise(SIGINT);\r\n\tprintf(\"givenPassword: %s\\n\", givenPassword);\r\n\tprintf(\"realPassword: %s\\n\", realPassword);\r\n\treturn 0;\r\n}",
                coding_languages=['CPP'],
                languages=['ENG'],
                categories=['SEC'],
                user=u,
                timestamp=now - timedelta(hours=2)
            )
            cr.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Code Reviews initiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            # initiate some tickets
            self.stdout.write('Initiating some helpdesk tickets...')
            now = timezone.now()

            t = Ticket(
                description='My code review got banned...',
                ticket_type='CODE_REVIEWS',
                base_user=u
            )
            t.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Helpdesk tickets created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        try:
            # initiate some badges
            self.stdout.write('Creating some achievement badges...')
            now = timezone.now()

            ach = Achievement(
                title='Django Newbie',
            )
            ach.badge.save('dj1.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/dj1.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='PY',
                experience_point=200,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='BE',
                experience_point=200,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='DB',
                experience_point=200,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Django Enthusiast',
            )
            ach.badge.save('dj2.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/dj2.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='PY',
                experience_point=600,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='BE',
                experience_point=600,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='DB',
                experience_point=600,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Django Expert',
            )
            ach.badge.save('dj3.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/dj3.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='PY',
                experience_point=800,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='BE',
                experience_point=1500,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='DB',
                experience_point=200,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Frontend Rookie',
            )
            ach.badge.save('fe1.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/fe1.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=300,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='HTML',
                experience_point=200,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='CSS',
                experience_point=200,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=200,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Frontend Developer',
            )
            ach.badge.save('fe2.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/fe2.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=1200,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='HTML',
                experience_point=800,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='CSS',
                experience_point=800,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=800,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Frontend Sexpert',
            )
            ach.badge.save('fe3.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/fe3.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=40000,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='HTML',
                experience_point=40000,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='CSS',
                experience_point=40000,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=40000,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Pretty good at Javascript',
            )
            ach.badge.save('js1.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/js1.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=250,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=500,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Pretty darn good at Javascript',
            )
            ach.badge.save('js2.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/js2.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=500,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=800,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='Pretty damn good at Javascript',
            )
            ach.badge.save('js3.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/js3.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=800,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=1800,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='React Rookie',
            )
            ach.badge.save('r1.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/r1.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=200,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=500,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='HTML',
                experience_point=300,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='CSS',
                experience_point=300,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='React-Ready',
            )
            ach.badge.save('r2.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/r2.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=500,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=800,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='HTML',
                experience_point=500,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='CSS',
                experience_point=500,
                achievement=ach,
            ).save()

            ach = Achievement(
                title='React Ragnarok',
            )
            ach.badge.save('r3.png', ImageFile(open('./codeine_django/common/management/demo_assets/badges/r3.png', 'rb')))
            ach.save()

            AchievementRequirement(
                stat='FE',
                experience_point=2000,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='JS',
                experience_point=5000,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='HTML',
                experience_point=2000,
                achievement=ach,
            ).save()
            AchievementRequirement(
                stat='CSS',
                experience_point=2000,
                achievement=ach,
            ).save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Achievement badges created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except
    # end def
