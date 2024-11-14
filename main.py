#!/usr/bin/env python

import requests
import re
import json
from todoist_api_python.api import TodoistAPI
from requests.auth import HTTPDigestAuth
from datetime import datetime, timezone, timedelta
import time
from random import randint
from database import DB

class CanvasAPI:
    def __init__(self):
        self.header = {}
        self.param = {"per_page": "100", "include": "submission", "enrollment_state": "active"}
        self.course_ids = []
        self.courses_id_name_dict = {}
        self.assignments = []

        with open("config.json") as config_file:
            self.config = json.load(config_file)
            
        self.header.update({"Authorization": f'Bearer {self.config["canvas_api_key"].strip()}'})

    def get_courses(self):
        try:
            self.response = requests.get(
                f"{self.config['canvas_api_heading']}/api/v1/courses",
                headers=self.header,
                params=self.param,
            )

            if self.response.status_code == 401:
                self.get_courses()
                return
            
            if self.config["courses"]:
                self.course_ids.extend(
                    list(map(lambda course_id: int(course_id), self.config["courses"]))
                )

                for course_id in self.course_ids:
                    response = requests.get(f'https://canvas.instructure.com/api/v1/courses/{course_id}', headers=self.header, params=self.param)
                    response.raise_for_status()
                    self.courses_id_name_dict[course_id] = re.sub(
                        r"[^-a-zA-Z0-9._\s]", " ", response.json()["name"]
                    )
                return

        except Exception:
            self.get_courses()
            return

    def get_assignments(self):
        try:
            for course_id in self.course_ids:
                url = f"{self.config['canvas_api_heading']}/api/v1/courses/{course_id}/assignments"
                while url:
                    response = requests.get(url, headers=self.header, params=self.param)
                    response.raise_for_status()
                    self.assignments.extend(response.json())
                    if "next" in response.links:
                        url = response.links["next"]["url"]
                    else:
                        url = None
            return self.assignments
                    
        except Exception:
            self.get_assignments()
            return

class TodoistAPIComm:
    def __init__(self):
        self.tasks = []
        self.projects = {}

        with open("config.json") as config_file:
            self.config = json.load(config_file)

        self.todoist_api = TodoistAPI(self.config["todoist_api_key"].strip())

    def get_tasks(self):
        self.tasks.extend(self.todoist_api.get_tasks())
        print(self.tasks)

    def get_projects(self):
        projects = self.todoist_api.get_projects()
        for project in projects:
            self.projects[project.name] = project.id
        print(self.projects)

    def transfer_tasks(self):
        pass

    def update_tasks(self):
        pass

    def create_task(self):
        pass

def update_db(assignments):
    for assignment in assignments:
        print(assignment['updated_at'])
        print('---------------------------------')

def organise_tasks():
    pass

if __name__ == "__main__":
    db = DB()
    if not db.check:
        db.init_db()
    
    canvas_api = CanvasAPI()
    canvas_api.get_courses()
    assignments = canvas_api.get_assignments()

    update_db(assignments)
    '''
    todoist_api = TodoistAPIComm()
    todoist_api.get_projects()
    # Create todoist projects?
    todoist_api.get_tasks() # Last 2 days of completed tasks

    organise_tasks()

    todoist_api.transfer_tasks()'''