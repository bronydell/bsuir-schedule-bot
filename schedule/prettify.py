def prettify_cabinet(cabinet):
    return cabinet


def teacher_name(teacher):
    return "{first_name} {middle_name} {last_name}".format(
        first_name=teacher['firstName'],
        middle_name=teacher['middleName'],
        last_name=teacher['lastName'],
    )


def get_lesson_type(lesson_type, lesson_types):
    try:
        return lesson_types[lesson_type]
    except KeyError:
        return lesson_type


def prettify_lesson(lesson, template, lesson_types):
    if lesson['numSubgroup'] == 0:
        return template.format(
            start_time=lesson['startLessonTime'],
            finish_time=lesson['endLessonTime'],
            type=get_lesson_type(lesson['lessonType'], lesson_types),
            subject=lesson['subject'],
            note=lesson['note'],
            teacher_name=teacher_name(lesson['employee'][0]),
            cabinet=prettify_cabinet(lesson['auditory'][0])
        )


def prettify_schedule(schedule, template, lesson_types):
    prettified_lessons = map(lambda lesson:
                             prettify_lesson(lesson, template, lesson_types),
                             schedule)
    pretty_text = '\n'.join(prettified_lessons)
    return pretty_text
