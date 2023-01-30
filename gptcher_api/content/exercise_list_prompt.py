prompt = """Suggest a detailed list of 40 topics for exercises for a beginner <language> student to learn about. Each exercise will contain sentences that the student learns to translate. 
For each topic, specify the topic, content description, and grammar focus in JSON. An exercise may also focus on new vocabulary, e.g. an exercise about occupations or countries.

Example:
[
    {
        "id": 0
        "topic": "Introducing yourself: first verbs and words",
        "content-description": "conversation between Alice and Bob",
        "grammar": null,
        "trains_vocabulary": false
    },
    ...
]

Output:"""

prefix = """[
    {"""
