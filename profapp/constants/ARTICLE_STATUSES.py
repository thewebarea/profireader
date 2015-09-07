from .USER_ROLES import RIGHTS


class ARTICLE_STATUS_IN_COMPANY:
    submitted = 'submitted'
    accepted = 'accepted'
    declined = 'declined'

    @classmethod
    def can_user_change_status_to(cls, from_status):
        if from_status == cls.submitted:
            return [cls.accepted, cls.declined]

        elif from_status == cls.accepted:
            return [cls.declined]

        elif from_status == cls.declined:
            return [cls.accepted]

        else:
            return [cls.accepted, cls.declined]

class ARTICLE_STATUS_IN_PORTAL:

    published = 'published'
    not_published = 'not_published'
    declined = 'declined'
