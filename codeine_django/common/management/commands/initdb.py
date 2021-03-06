from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone

from common.models import BaseUser, Member, Partner, Organization, BankDetail
from courses.models import (
    Course,
    Chapter,
    CourseMaterial,
    CourseFile,
    Video,
    CourseReview,
    Quiz,
    Question,
    ShortAnswer,
    MCQ,
    MRQ,
    CourseComment
)
from consultations.models import ConsultationSlot

import sys
from datetime import timedelta


class Command(BaseCommand):
    help = 'Prepopulates the database with data for demo'

    def handle(self, *args, **options):
        # raise CommandError('Error')
        # self.stdout.write('Hello' + self.style.SUCCESS('Success'))

        # global refs
        admin = None

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
            u = BaseUser.objects.create_user(
                'm1@m1.com',
                'password',
                first_name='Jack',
                last_name='Johnson',
                is_active=True
            )
            u.profile_photo.save('m1.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/m1.jpeg', 'rb')))
            u.save()

            m = Member(user=u)
            m.save()

            u = BaseUser.objects.create_user(
                'm2@m2.com',
                'password',
                first_name='Suzuki',
                last_name='Haneda',
                is_active=True
            )
            u.profile_photo.save('m2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/m2.jpeg', 'rb')))
            u.save()

            m = Member(user=u)
            m.save()
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
                first_name='Vanessa',
                last_name='Fred',
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

            c = Course(
                title='React Native for Beginners',
                learning_objectives=['React Native Novice to Ninja!', 'Create a React Native app from Scratch'],
                requirements=['Node Package Manager', 'Basic Javascript Knowledge'],
                description='Hey gang, and welcome to your first React Native tutorial for beginners. In this series we\'ll go from novice to ninja and create a React Native app from scratch. First though, we\'ll get set up and talk about what React Native actually is.',
                introduction_video_url='https://www.youtube.com/watch?v=ur6I5m2nTvk',
                coding_languages=['JS', 'HTML', 'CSS'],
                languages=['ENG'],
                categories=['FE', 'UI'],
                is_published=True,
                published_date=timezone.now(),
                exp_points=230,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course1/courseimage.png', 'rb')))
            c.save()

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

            q = Quiz(
                course_material=cm,
                passing_marks=0,
            )
            q.save()

            qn = Question(
                title='How do you start your local development server?',
                subtitle='Hint: it\'s the same with ReactJS',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['npm install <package>', 'npm i <package>', 'npm run <package>', 'npm <package>'],
                correct_answer=['npm install <package>', 'npm i <package>']
            )
            mrq.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

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

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qn = Question(
                title='How do you start your local development server?',
                subtitle='Hint: it\'s the same with ReactJS',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['npm install <package>', 'npm i <package>', 'npm run <package>', 'npm <package>'],
                correct_answer=['npm install <package>', 'npm i <package>']
            )
            mrq.save()

            qn = Question(
                title='Who is the creator of these videos?',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Net', 'Ninja', 'NetNinja']
            )
            sa.save()

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
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course2/course2.jpg', 'rb')))
            c.save()

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

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

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
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course3/course3.png', 'rb')))
            c.save()

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

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

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
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course4/course4.png', 'rb')))
            c.save()

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

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

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
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course5/course5.png', 'rb')))
            c.save()

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

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

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
                exp_points=600,
                partner=partner
            )
            c.thumbnail.save('courseimage.png', ImageFile(open('./codeine_django/common/management/demo_assets/course6/course6.png', 'rb')))
            c.save()

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

            q = Quiz(
                course=c,
                passing_marks=1,
            )
            q.save()

            qn = Question(
                title='Which of the following are machine learning algorithms',
                subtitle='You should know this...',
                order=q.questions.count(),
                quiz=q
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
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            mrq = MRQ(
                question=qn,
                marks=1,
                options=['Handsome', 'Very Handsome', 'Extremely Handsome', 'Ugly'],
                correct_answer=['Ugly']
            )
            mrq.save()

            qn = Question(
                title='Who is Andrew Ng',
                order=q.questions.count(),
                quiz=q
            )
            qn.save()

            sa = ShortAnswer(
                question=qn,
                marks=1,
                keywords=['Pope']
            )
            sa.save()

            self.stdout.write(f'{self.style.SUCCESS("Success")}: Infosec Course created')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except

        # create course comments
        self.stdout.write('Creating some comments...')
        try:
            chap = Chapter.objects.get(title='React Native App Basics')
            cm = chap.course_materials.all()[0]
            user = BaseUser.objects.get(first_name='Steve')

            cc = CourseComment(
                display_id=cm.course_comments.count() + 1,
                comment='This is great!!!',
                course_material=cm,
                user=user,
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
            now = timezone.now()

            cs = ConsultationSlot(
                title='React Native 1',
                start_time=(now + timedelta(days=2)).replace(hour=2, minute=0),
                end_time=(now + timedelta(days=2)).replace(hour=2, minute=30),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=0,
                max_members=2,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 2',
                start_time=(now + timedelta(days=2)).replace(hour=3, minute=0),
                end_time=(now + timedelta(days=2)).replace(hour=4, minute=0),
                meeting_link='https://meet.google.com/meo-fymy-oae',
                price_per_pax=5,
                max_members=2,
                partner=p
            )
            cs.save()

            cs = ConsultationSlot(
                title='React Native 3',
                start_time=(now + timedelta(days=3)).replace(hour=10, minute=0),
                end_time=(now + timedelta(days=3)).replace(hour=11, minute=30),
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
        except:
            e = sys.exc_info()[0]
            self.stdout.write(f'{self.style.ERROR("ERROR")}: {repr(e)}')
        # end try-except
    # end def
