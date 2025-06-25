
'''
Multi-agent tutoring workflow based on "SOPs"

TutorManager
    - accepts or rejects request
    - analyzes the content and inquiry to generate SOP (study plan)
    - select appropriate sub agents based on content and student inquiry
    - tool use: none

TutorGrammar
    - accesses content for interesting grammar points to teach
    - can work in parallel with other sub agents, reports to the TutorManager
    - tool use: access-grammar-kb

TutorNewWords
    - accesses content for new words, takes into account students learned words
    - tool-use: none

TutorQuestionGen
    - based on the content creates 2-3 sentences based on the article's content
    - tool: none

TutorCulture
    - accesses the article for relevant cultural context to share with student

TutorRapport
    - offer encouragement and niceties

TutorVoiceGen
    - creates voice audio based on other agents generations
    - tools: generate-voice, upload-s3

think about workflows vs. agents
'''

class Role():
    name: str = ""

    def get_role_memories():
        pass

    def send_memories_pool():
        '''
        sends document to shared memory store
        '''
        pass


class TutorManager(Role):

    name: str = "Mabel"
    profile: str = "Tutor (Manager)"
    goals: str = (
        ""
    )
    constraints: str = "use the student's native language for all explainations"

    student_question: str = "help me understand this content"
    content: str = ""

    available_subagents = ['TutorNewWords', 'TutorGrammar', 'TutorQuestionGen', 'TutorCulture', 'TutorRapport']

    reject_accept_request = '''
    Your job is to decide if the students question is appropriate based on the provided content.

    Student Question: {student_question}

    Content: {content}

    If the question is not relevant, unrelated, harmful, or inappropriate, respond with NO. Otherwise respond with YES. Just respond with single word YES or NO only.
    '''
    choose_sub_agents_prompt = '''
    Your job is to choose the appropriate sub agents for the job based on the available choices. Consider both the provided "Content" and "Student Question" when choosing workers.

    '''

    def __init__(self, question: str, content: str) -> None:
        self.student_question = question
        self.content = content

    def get_students_context():
        pass

    def reject_pass_request() -> bool:

        return True

    def choose_sub_agents() -> None:
        '''
        uses content and student's question to choose sub agents
        '''
        pass

    def analyze_content_question(self):
        '''
        thinks about the content and student's inquiry at a high-level, generates a lesson
        plan to be shared with other sub agents
        '''
        pass

    def run(self, request):
        pass


class TutorNewWords(Role):

    name: str = "Mabel"
    profile: str = "Tutor (NewWords)"
    goals: str = (
        ""
    )

    generate_new_words_prompt = '''
    Based on the Lesson Plan and Content, identify 10 new Chinese words that would be helpful for the student to learn.

    Lesson Plan: {lesson_plan}

    Content: {content}

    Any new words should be from the provided content only and nowhere else.
    '''

    def generate_new_words():
        pass

    def run(self):
        pass
