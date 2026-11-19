/*
 * Лабораторная работа 10
 * Логическое программирование в SWI-Prolog
 * Индивидуальный вариант 1: «Стипендия»
 *
 * Файл: lab10.pl
 * Среда: SWI-Prolog 9 или новее
 *
 * Содержит исходную учебную базу из методички, все восемь основных
 * заданий и индивидуальный предикат eligible_for_grant/1.
 * Для проверки загрузите файл: ?- [lab10].
 */

% ------------------------------------------------------------------
% 1. ФАКТЫ: СТУДЕНТЫ И УЧЕБНЫЕ ДИСЦИПЛИНЫ
% ------------------------------------------------------------------

student(aida).
student(miras).
student(dana).
student(timur).
student(aliya).                 % Добавленный студент по заданию 1

course(programming_1).
course(programming_2).
course(data_structures).
course(databases).
course(artificial_intelligence).
course(machine_learning).

% completed(Student, Course): студент освоил дисциплину.
completed(aida, programming_1).
completed(aida, programming_2).
completed(aida, data_structures).
completed(aida, databases).

completed(miras, programming_1).
completed(miras, databases).

completed(dana, programming_1).
completed(dana, programming_2).
completed(dana, data_structures).

completed(timur, programming_1).

% Два факта об освоенных дисциплинах добавленного студента.
completed(aliya, programming_1).
completed(aliya, databases).

% requires(Course, Prerequisite): непосредственная зависимость дисциплины.
requires(programming_2, programming_1).
requires(data_structures, programming_2).
requires(artificial_intelligence, data_structures).
requires(artificial_intelligence, databases).
requires(machine_learning, artificial_intelligence).

% ------------------------------------------------------------------
% 2. ПРАВИЛА: СОСТАВНЫЕ УСЛОВИЯ
% ------------------------------------------------------------------

% Кандидат на курс ИИ должен освоить структуры данных и базы данных.
ai_candidate(Student) :-
    student(Student),
    completed(Student, data_structures),
    completed(Student, databases).

% Подготовленный студент освоил programming_2 и data_structures.
strong_student(Student) :-
    student(Student),
    completed(Student, programming_2),
    completed(Student, data_structures).

% ------------------------------------------------------------------
% 3. УНИФИКАЦИЯ
% ------------------------------------------------------------------

% Для демонстрации унификации используются запросы к составным термам:
% ?- record(Name, Course) = record(aida, databases).
% ?- pair(X, X) = pair(aida, miras).       % ожидается false
% ?- [Head|Tail] = [programming_1, databases, ai].
% Эти выражения являются запросами SWI-Prolog, а не правилами базы.

% ------------------------------------------------------------------
% 4. НЕПОСРЕДСТВЕННЫЙ ДОПУСК К ДИСЦИПЛИНЕ
% ------------------------------------------------------------------

% Недостающий непосредственный пререквизит.
missing_direct(Student, Course, Prerequisite) :-
    student(Student),
    course(Course),
    requires(Course, Prerequisite),
    \+ completed(Student, Prerequisite).

% Допуск по непосредственным пререквизитам.
% Если у дисциплины нет requires/2, обязательных пререквизитов нет.
immediate_eligible(Student, Course) :-
    student(Student),
    course(Course),
    \+ missing_direct(Student, Course, _).

% ------------------------------------------------------------------
% 5. ТРАНЗИТИВНЫЕ ПРЕРЕКВИЗИТЫ (РЕКУРСИЯ)
% ------------------------------------------------------------------

% Базовый случай: непосредственный пререквизит.
prerequisite(Course, Prerequisite) :-
    requires(Course, Prerequisite).

% Рекурсивный случай: пререквизит пререквизита.
prerequisite(Course, Prerequisite) :-
    requires(Course, Intermediate),
    prerequisite(Intermediate, Prerequisite).

% ------------------------------------------------------------------
% 6. ПОЛНЫЙ ДОПУСК И СПИСОК НЕДОСТАЮЩИХ ДИСЦИПЛИН
% ------------------------------------------------------------------

% Безопасная версия транзитивного обхода с контролем посещённых узлов.
safe_prerequisite(Course, Prerequisite) :-
    safe_prerequisite(Course, Prerequisite, [Course]).

safe_prerequisite(Course, Prerequisite, Visited) :-
    requires(Course, Prerequisite),
    \+ memberchk(Prerequisite, Visited).

safe_prerequisite(Course, Prerequisite, Visited) :-
    requires(Course, Next),
    \+ memberchk(Next, Visited),
    safe_prerequisite(Next, Prerequisite, [Next|Visited]).

% missing_all/3 возвращает отсортированный список уникальных
% отсутствующих прямых и косвенных пререквизитов.
% findall/3 корректно возвращает [] даже при отсутствии результатов.
missing_all(Student, Course, Missing) :-
    student(Student),
    course(Course),
    findall(Prerequisite,
            ( safe_prerequisite(Course, Prerequisite),
              \+ completed(Student, Prerequisite)
            ),
            Unsorted),
    sort(Unsorted, Missing).

% Полный допуск: список недостающих дисциплин должен быть пустым.
eligible(Student, Course) :-
    student(Student),
    course(Course),
    missing_all(Student, Course, []).

% ------------------------------------------------------------------
% 7. ИНДИВИДУАЛЬНЫЙ ВАРИАНТ 1: СТИПЕНДИЯ
% ------------------------------------------------------------------

% grade(Student, Course, Score): оценка студента по дисциплине.
% Критерий модели: все выставленные оценки не ниже 85 баллов.
grade(aida, programming_1, 92).
grade(aida, programming_2, 90).
grade(aida, data_structures, 88).
grade(aida, databases, 95).

grade(miras, programming_1, 90).
grade(miras, databases, 84).

grade(dana, programming_1, 86).
grade(dana, programming_2, 91).
grade(dana, data_structures, 88).

grade(timur, programming_1, 94).
grade(timur, databases, 90).

grade(aliya, programming_1, 89).
grade(aliya, databases, 87).

% Факт академической задолженности.
academic_debt(timur).

% Порог для получения стипендии в рамках учебной модели.
grant_min_grade(85).

% У студента должна быть хотя бы одна оценка.
has_grades(Student) :-
    grade(Student, _, _).

% Все оценки студента должны быть не ниже установленного порога.
grades_meet_grant_requirement(Student) :-
    grant_min_grade(Minimum),
    has_grades(Student),
    \+ ( grade(Student, _, Score),
         Score < Minimum
       ).

% Отсутствие академической задолженности.
no_academic_debts(Student) :-
    student(Student),
    \+ academic_debt(Student).

% Основной предикат индивидуального варианта.
% Стипендия назначается при наличии оценок требуемого уровня
% и полном отсутствии академических задолженностей.
eligible_for_grant(Student) :-
    student(Student),
    grades_meet_grant_requirement(Student),
    no_academic_debts(Student).

% ------------------------------------------------------------------
% 8. ИНТЕГРИРОВАННАЯ РЕКОМЕНДАЦИЯ
% ------------------------------------------------------------------

% Возвращает eligible с пустым списком либо missing со списком долгов.
recommendation(Student, Course, eligible, []) :-
    eligible(Student, Course).

recommendation(Student, Course, missing, Missing) :-
    missing_all(Student, Course, Missing),
    Missing \= [].

% ------------------------------------------------------------------
% ДЕМОНСТРАЦИОННЫЕ ЗАПРОСЫ (выполнять в консоли SWI-Prolog)
% ------------------------------------------------------------------
%
% Задание 1 — факты:
% ?- completed(aida, databases).
% ?- completed(Student, programming_1).
% ?- completed(aliya, databases).
% ?- completed(aliya, machine_learning).          % false
%
% Задание 2 — правила:
% ?- ai_candidate(Student).
% ?- strong_student(Student).
%
% Задание 3 — унификация:
% ?- record(Name, Course) = record(aida, databases).
% ?- pair(X, X) = pair(aida, miras).              % false
% ?- [Head|Tail] = [programming_1, databases, ai].
%
% Задание 4 — непосредственный допуск:
% ?- missing_direct(miras, artificial_intelligence, What).
% ?- immediate_eligible(aida, artificial_intelligence).
% ?- immediate_eligible(miras, artificial_intelligence). % false
%
% Задание 5 — транзитивные зависимости:
% ?- prerequisite(artificial_intelligence, programming_1).
% ?- setof(Course, prerequisite(machine_learning, Course), Courses).
%
% Задание 6 — полный допуск:
% ?- missing_all(miras, artificial_intelligence, Missing).
% ?- eligible(aida, artificial_intelligence).
%
% Задание 7 — защита рекурсии:
% Для эксперимента временно добавьте в консоли:
% ?- assertz(requires(programming_1, machine_learning)).
% ?- setof(P, safe_prerequisite(machine_learning, P), Ps).
% После эксперимента удалите добавленный факт:
% ?- retract(requires(programming_1, machine_learning)).
% В постоянной базе циклического факта нет.
%
% Задание 8 — рекомендации:
% ?- recommendation(miras, artificial_intelligence, Status, Missing).
% ?- recommendation(Student, machine_learning, Status, Missing).
%
% Индивидуальный вариант 1 — стипендия:
% ?- eligible_for_grant(aida).                    % true
% ?- eligible_for_grant(miras).                   % false: оценка 84
% ?- eligible_for_grant(timur).                   % false: задолженность
% ?- eligible_for_grant(aliya).                   % true
% ?- findall(Student, eligible_for_grant(Student), Students).
%
% Примечание: порог 85 баллов — явно заданное допущение учебной модели,
% поскольку методичка требует учитывать оценки и задолженности, но не задаёт
% конкретное числовое значение проходного балла.
