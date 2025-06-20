from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class TimeStampedModelWithUser(models.Model):
    """
    Classe abstraite pour le suivi automatique des créations et modifications
    avec utilisateur associé.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        verbose_name=_("Créé par")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de mise à jour"))
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        verbose_name=_("Modifié par")
    )

    class Meta:
        abstract = True


class School(TimeStampedModelWithUser):
    """
    Modèle représentant un établissement scolaire.
    """
    name = models.CharField(max_length=255, verbose_name=_("Nom de l'établissement"))
    ville = models.CharField(max_length=100, verbose_name=_("Ville"))
    quartier = models.CharField(max_length=100, verbose_name=_("Quartier"))
    logo = models.ImageField(
        upload_to="school_logos/",
        default="defaults/school_logo.png",
        blank=True,
        verbose_name=_("Logo de l'établissement")
    )
    document_header = models.ImageField(
        upload_to="school_headers/",
        blank=True,
        null=True,
        verbose_name=_("En-tête des documents")
    )
    foundation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de fondation")
    )

    class Meta:
        verbose_name = _("Établissement scolaire")
        verbose_name_plural = _("Établissements scolaires")
        unique_together = ('name', 'ville', 'quartier')

    def __str__(self):
        return f"{self.name} - {self.quartier}, {self.ville}"


class SchoolYear(models.Model):
    school = models.ForeignKey("School", on_delete=models.CASCADE, related_name="school_years", verbose_name=_("Établissement"))
    start_date = models.DateField(verbose_name=_("Date de début"))
    end_date = models.DateField(verbose_name=_("Date de fin"), blank=True)

    name = models.CharField(max_length=20, editable=False, verbose_name=_("Nom de l'année scolaire"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="created_school_years",
        verbose_name=_("Créé par")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Mis à jour le"))
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="updated_school_years",
        verbose_name=_("Mis à jour par")
    )

    class Meta:
        verbose_name = _("Année scolaire")
        verbose_name_plural = _("Années scolaires")
        unique_together = ("school", "name")
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        if self.start_date and not self.end_date:
            # Automatically set end_date to start_date + 1 year
            self.end_date = self.start_date.replace(year=self.start_date.year + 1)

        # Generate the name like "2024-2025"
        if self.start_date and self.end_date:
            self.name = f"{self.start_date.year}-{self.end_date.year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.school})"


class Grade(TimeStampedModelWithUser):
    # L'école à laquelle appartient ce cycle
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name=_("École")
    )

    # Le nom du cycle scolaire : ex. Primaire, Collège, Lycée
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom du cycle")
    )

    has_option = models.BooleanField(
            default=False,
            verbose_name=_("A des options"),
            help_text=_("Si cest possible d'avoir des options")
            )

    # Abréviation facultative : ex. PRI, COL, LYC
    abbreviation = models.CharField(
        max_length=20,
        verbose_name=_("Abréviation"),
        blank=True
    )

    # Ordre d'affichage logique (ex: Primaire = 1, Collège = 2, etc.)
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Ordre d'affichage"),
        help_text=_("Numéro pour organiser les grades")
    )

    class Meta:
        verbose_name = _("Cycle")
        verbose_name_plural = _("Cycles")
        # Une même école ne peut pas avoir deux cycles avec le même nom
        unique_together = [("school", "name")]
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.school})"




class GradeOption(TimeStampedModelWithUser):
    """
    Représente une option spécifique à un cycle éducatif (Grade), 
    par ex. : Sciences, Lettres, Techniques.
    """
    grade = models.ForeignKey(
        "Grade",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("Cycle")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom de l'option")
    )
    abbreviation = models.CharField(
        max_length=20,
        verbose_name=_("Abréviation"),
        blank=True
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Ordre"),
        help_text=_("Numéro pour organiser les options")
    )

    class Meta:
        verbose_name = _("Option du cycle")
        verbose_name_plural = _("Options des cycles")
        unique_together = [("grade", "name")]
        ordering = ["grade", "order"]

    def __str__(self):
        return f"{self.name} ({self.grade})"


class Level(TimeStampedModelWithUser):
    """
    Représente un niveau d'étude dans un cycle (Grade), ex: 6e, 5e, Terminale.
    """
    grade = models.ForeignKey(
        "Grade",
        on_delete=models.CASCADE,
        related_name="levels",
        verbose_name=_("Cycle")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom du niveau")
    )
    abbreviation = models.CharField(
        max_length=20,
        verbose_name=_("Abréviation"),
        blank=True
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Ordre"),
        help_text=_("Numéro pour organiser les niveaux")
    )

    class Meta:
        verbose_name = _("Niveau")
        verbose_name_plural = _("Niveaux")
        unique_together = [("grade", "name")]
        ordering = ["grade", "order"]

    def __str__(self):
        return f"{self.name} ({self.grade})"

class SchoolYearLevel(TimeStampedModelWithUser):
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name='schoolyear_levels',
        verbose_name=_("Année scolaire"),
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='schoolyear_levels',
        verbose_name=_("Cycle (Grade)"),
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='schoolyear_levels',
        verbose_name=_("Niveau (Classe)"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Actif ?"),
        help_text=_("Active ou désactive ce niveau pour cette année scolaire.")
    )

    class Meta:
        verbose_name = _("Niveau scolaire annuel")
        verbose_name_plural = _("Niveaux scolaires annuels")
        unique_together = ('school_year', 'level')

    def clean(self):
        # Validation 1 : le niveau sélectionné appartient bien au grade sélectionné
        if self.level.grade != self.grade:
            raise ValidationError(_("Le niveau sélectionné n'appartient pas au cycle spécifié."))

        # Validation 2 : le cycle appartient à la même école que l’année scolaire
        if self.grade.school != self.school_year.school:
            raise ValidationError(_("Le cycle sélectionné n'appartient pas au même établissement que l'année scolaire."))

    def __str__(self):
        return f"{self.level} ({self.school_year})"

class Classroom(TimeStampedModelWithUser):
    school_year_level = models.ForeignKey(
        'SchoolYearLevel',
        on_delete=models.CASCADE,
        related_name='classrooms',
        verbose_name=_("niveau annuel"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("nom de la classe"),
        help_text=_("Ex: Terminale A, 6ème B"),
    )
    grade_option = models.ForeignKey(
        'GradeOption',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classrooms',
        verbose_name=_("option"),
        help_text=_("Option du grade, ex: Sciences, Lettres..."),
    )

    class Meta:
        verbose_name = _("classe")
        verbose_name_plural = _("classes")
        unique_together = (
            ('school_year_level', 'name', 'grade_option'),
        )

    def clean(self):
        from django.core.exceptions import ValidationError

        # Vérifie que l'option est requise si le grade a des options
        has_option = self.school_year_level.grade.has_option
        if has_option and not self.grade_option:
            raise ValidationError(_("Cette classe requiert une option."))
        if not has_option and self.grade_option:
            raise ValidationError(_("Cette classe ne doit pas avoir d'option."))

        # Vérifie que l'option correspond au grade
        if self.grade_option and self.grade_option.grade != self.school_year_level.grade:
            raise ValidationError(_("L'option ne correspond pas au grade de ce niveau."))

    def __str__(self):
        if self.grade_option:
            return f"{self.school_year_level.level.name} {self.grade_option.abbreviation} {self.name}"
        return f"{self.school_year_level.level.name} - {self.name}"



class Subject(TimeStampedModelWithUser):
    """
    Représente une matière définie pour une année scolaire spécifique dans un établissement donné.
    Exemple : 'Mathématiques' pour l'année 2024-2025 du Collège Sainte-Marie.
    """
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name=_("Année scolaire")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom de la matière")
    )

    class Meta:
        verbose_name = _("Matière annuelle")
        verbose_name_plural = _("Matières annuelles")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["school_year", "name"],
                name="unique_subject_per_year"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.school_year.name})"


class ClassroomSubject(TimeStampedModelWithUser):
    """
    Lien entre une matière et une classe pour une année scolaire,
    avec un coefficient et potentiellement un enseignant assigné.
    """
    classroom = models.ForeignKey(
        "core.Classroom",
        on_delete=models.CASCADE,
        related_name="classroom_subjects",
        verbose_name=_("Classe")
    )
    subject = models.ForeignKey(
        "core.Subject",
        on_delete=models.CASCADE,
        related_name="classroom_subjects",
        verbose_name=_("Matière")
    )
    coefficient = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0.01)],
        verbose_name=_("Coefficient")
    )

    class Meta:
        verbose_name = _("Matière en classe")
        verbose_name_plural = _("Matières en classe")
        constraints = [
            models.UniqueConstraint(
                fields=["classroom", "subject"],
                name="unique_subject_per_classroom"
            )
        ]

    def clean(self):
        # Vérifier la correspondance des écoles et années scolaires
        classroom_sy = self.classroom.school_year_level.school_year
        subject_sy = self.subject.school_year

        if subject_sy != classroom_sy:
            raise ValidationError(
                _("La matière et la classe doivent appartenir à la même année scolaire.")
            )

        if subject_sy.school != classroom_sy.school:
            raise ValidationError(
                _("La matière et la classe doivent appartenir au même établissement.")
            )

        if self.coefficient <= 0:
            raise ValidationError(
                _("Le coefficient doit être un nombre positif.")
            )

    def __str__(self):
        return f"{self.subject.name} - {self.classroom.name}"


class Teacher(TimeStampedModelWithUser):
    """
    Représente un enseignant pour une année scolaire donnée.
    Un même utilisateur peut être enseignant dans plusieurs écoles, mais pas dans la même SchoolYear.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profiles",
        verbose_name=_("Utilisateur"),
    )
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name="teachers",
        verbose_name=_("Année scolaire"),
    )

    class Meta:
        verbose_name = _("Enseignant")
        verbose_name_plural = _("Enseignants")
        unique_together = ("user", "school_year")  # Un enseignant par année scolaire

    def __str__(self):
        return f"{self.user.first_name} - {self.school_year.name}"

    def clean(self):
        # Vérifie que l'utilisateur appartient bien à l'école de l'année scolaire
        if hasattr(self.user, "student_profiles"):
            if self.user.student_profiles.filter(school_year=self.school_year).exists():
                raise ValidationError(
                    _("Un utilisateur ne peut pas être enseignant dans une année scolaire où il est élève.")
                )

class Student(TimeStampedModelWithUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students', verbose_name=_("Classe"))
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='students', verbose_name=_("Année scolaire"))
    enrollment_number = models.CharField(_("Numéro d'inscription"), max_length=30, unique=True)

    class Meta:
        unique_together = ('user', 'schoolyear')
        verbose_name = _("Élève")
        verbose_name_plural = _("Élèves")

    def clean(self):
        if self.classroom.school_year_level.school_year != self.schoolyear:
            raise ValidationError(_("La classe sélectionnée ne correspond pas à l'année scolaire de l'inscription."))

        if self.classroom.school_year_level.grade.school != self.schoolyear.school:
            raise ValidationError(_("La classe ne correspond pas à l’école de l’année scolaire."))

        # Vérifier que l'utilisateur n'est pas enseignant dans cette même classe
        teacher_profile = getattr(self.user, 'teacher_profile', None)
        if teacher_profile:
            from core.models import ClassroomSubject
            is_teacher_here = ClassroomSubject.objects.filter(
                classroom=self.classroom,
                teacher=teacher_profile
            ).exists()
            if is_teacher_here:
                raise ValidationError(_("Un utilisateur ne peut pas être enseignant dans une classe où il est aussi élève."))

    def __str__(self):
        return f"{self.user.first_name} - {self.classroom} - {self.schoolyear.name}"






