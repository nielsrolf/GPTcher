"""
ContentCreator creates LearnSets and suggests matching LearnSets for a given user.
"""
import json
import os
import re
from dataclasses import dataclass
from functools import cache
from typing import List

import click
import deepl
from dotenv import load_dotenv

from gptcher.content import exercise_create_prompt, exercise_list_prompt
from gptcher.language_codes import code_of
from gptcher.utils import complete_and_parse_json, supabase

load_dotenv(override=True)
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)


def read_and_save_voice(text, language):
    pass


def remove_prefix(s):
    return re.sub(r"^\d+\.\s*", "", s)


def translate(text, language):
    try:
        return translator.translate_text(
            text, target_lang=code_of[language], formality="less"
        ).text
    except:
        return translator.translate_text(text, target_lang=code_of[language]).text


def create_content(language):
    exercises = create_exercise_list(language)
    for exercise_description in exercises:
        create_exercise(language, exercise_description)


def create_exercise_list(language):
    prompt = exercise_list_prompt.prompt.replace("<language>", language)
    print(prompt)
    exercises = complete_and_parse_json(
        prompt, "\n\n", exercise_list_prompt.prefix, max_tokens=1000
    )
    return exercises


def create_exercise(language, exercise_description):
    """
    Creates one or more exercise for the escription.
    Completion is in this format:
    [
        "topic": <topic>,
        "content-description": <content-description>,
        "grammar": <grammar>,
        "exercise_number": <exercise_number, starting at 1>,
        "task_description": <initial message to the student>,
        "vocabulary_en": [<list of new words to train in this exercise>],
        "sentences_en": [<list of sentences the student has to translate. > ]
    },,...]

    """
    # check if it exists already
    if (
        supabase.table("exercises")
        .select("*")
        .eq("language", language)
        .eq("topic", exercise_description["topic"])
        .execute()
        .data
    ):
        print("Exercise already exists, skipping:", exercise_description["topic"])
        return
    exercise_json = json.dumps(exercise_description, indent=4)
    prompt = exercise_create_prompt.prompt.replace(
        "{exercise_json}", exercise_json
    ).replace("<language>", language)
    exercises_json = complete_and_parse_json(
        prompt, "\n\n", exercise_create_prompt.prefix, max_tokens=3000
    )
    for exercise_json in exercises_json:
        exercise = Exercise.create(language, **exercise_json)


@dataclass
class TranslationTask:
    language: str
    sentence_en: str
    sentence_translated: str
    voice: str
    id: str = None

    @staticmethod
    def create(language, sentence):
        task = TranslationTask(
            language,
            sentence,
            translate(sentence, language),
            read_and_save_voice(sentence, language),
        )
        task.to_db()
        return task

    def to_db(self):
        data = dict(**self.__dict__)
        if self.id is None:
            del data["id"]
        db_entry = supabase.table("translation_tasks").upsert(data).execute().data[0]
        self.id = db_entry["id"]
        return self

    def check_voice(self):
        """needed because of cache"""
        if self.voice is None:
            db_entry = (
                supabase.table("translation_tasks")
                .select("*")
                .eq("id", self.id)
                .execute()
                .data[0]["voice"]
            )
            self.voice = db_entry
        return self.voice

    @staticmethod
    @cache
    def from_db(task_id):
        print("Loading task from db:", task_id)
        db_entry = (
            supabase.table("translation_tasks")
            .select("*")
            .eq("id", task_id)
            .execute()
            .data[0]
        )
        task = TranslationTask(**db_entry)
        return task


@dataclass
class Exercise:
    language: str
    topic: str
    content_description: str
    grammar: str
    exercise_number: int
    task_description: str
    id: str = None
    user_id: str = None            
    
    @property
    def translation_tasks(self):
        if self.id:
            task_ids = (
                supabase.table("exercise_translation_tasks")
                .select("translation_task_id")
                .order("order")
                .eq("exercise_id", self.id)
                .execute()
                .data
            )
        translation_tasks = [
                TranslationTask.from_db(task["translation_task_id"])
                for task in task_ids
            ]
        return translation_tasks

    @staticmethod
    def create(
        language,
        topic,
        content_description,
        grammar,
        exercise_number,
        task_description,
        vocabulary_en,
        sentences_en,
        user_id=None,
    ):
        translation_tasks = [
            TranslationTask.create(language, sentence) for sentence in sentences_en
        ]
        exercise = Exercise(
            language,
            topic,
            content_description,
            grammar,
            exercise_number,
            task_description,
            user_id=user_id,
        )
        exercise.to_db()
        return exercise

    def to_db(self):
        data = dict(**self.__dict__)
        if not self.id:
            del data["id"]
        db_entry = supabase.table("exercises").insert(data).execute()
        self.id = db_entry.data[0]["id"]
        for i, task in enumerate(self.translation_tasks):
            supabase.table("exercise_translation_tasks").insert(
                {"exercise_id": self.id, "translation_task_id": task.id, "order": i}
            ).execute()

    @staticmethod
    @cache
    def from_db(exercise_id):
        db_entry = (
            supabase.table("exercises")
            .select("*")
            .eq("id", exercise_id)
            .execute()
            .data[0]
        )
        exercise = Exercise(**db_entry)
        return exercise


async def load_all_exercises(language):
    exercises = (
        supabase.table("exercises").select("*").eq("language", language).execute().data
    )
    exercises = [Exercise.from_db(exercise["id"]) for exercise in exercises]


@click.command()
@click.argument("language")
def cli(language):
    create_content(language)


def delete_language(language):
    # Get all exercises
    exercises = (
        supabase.table("exercises").select("*").eq("language", language).execute().data
    )
    for exercise in exercises:
        # Get all translation tasks
        tasks = (
            supabase.table("exercise_translation_tasks")
            .select("*")
            .eq("exercise_id", exercise["id"])
            .execute()
            .data
        )
        for task in tasks:
            # Delete the relation
            supabase.table("exercise_translation_tasks").delete().eq(
                "exercise_id", exercise["id"]
            ).execute()
            # Delete translation task
            supabase.table("translation_tasks").delete().eq(
                "id", task["translation_task_id"]
            ).execute()
        # Delete exercise
        supabase.table("exercises").delete().eq("id", exercise["id"]).execute()


if __name__ == "__main__":
    cli()
    # delete_language("German")
