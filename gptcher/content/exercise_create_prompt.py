prompt = """Create a list of exercises for a <language> student based on this JSON description of the exercise:

{exercise_json}

The exercise starts with a description of the exercise that is shown to the student. Then, it is followed by a number of translation tasks for the student. The output format is again in JSON, in the following format:
[
    {
        "topic": <topic>,
        "content_description": <content-description>,
        "grammar": <grammar>,
        "exercise_number": <exercise_number, starting at 1>,
        "task_description": <initial message to the student>,
        "vocabulary_en": [<list of new words to train in this exercise>],
        "sentences_en": [<list of 10-20 sentences the student has to translate.>]
    },
    ...
]
Create as many exercises as needed for this topic.

Output:
"""

prefix = """[
    {"""