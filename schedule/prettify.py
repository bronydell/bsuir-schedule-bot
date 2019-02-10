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


def get_subgroup(subgroup_template, subgroup):
    if subgroup == 0:
        return ''
    else:
        return subgroup_template.format(subgroup=subgroup)


def prettify_lesson(lesson, template, lesson_types, subgroup_template, nothing):
    teachers = nothing if len(lesson['employee']) == 0 else ', '.join(
        map(lambda employee: teacher_name(employee), lesson['employee']))
    cabinets = nothing if len(lesson['auditory']) == 0 else ', '.join(
        map(lambda cabinet: prettify_cabinet(cabinet), lesson['auditory']))
    api_note = '' if not lesson.get('note', None) else lesson['note']
    return template.format(
        subgroup=get_subgroup(subgroup_template, lesson['numSubgroup']),
        start_time=lesson['startLessonTime'],
        finish_time=lesson['endLessonTime'],
        type=get_lesson_type(lesson['lessonType'], lesson_types),
        subject=lesson['subject'],
        note=api_note,
        teacher_name=teachers,
        cabinet=cabinets
    )


def prettify_schedule(schedule, template, lesson_types, subgroup_template, nothing):
    prettified_lessons = map(lambda lesson:
                             prettify_lesson(lesson, template, lesson_types, subgroup_template, nothing),
                             schedule)
    pretty_text = '\n'.join(prettified_lessons)
    return pretty_text
