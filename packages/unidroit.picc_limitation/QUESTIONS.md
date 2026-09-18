# Вопросы к пакету `unidroit.picc_limitation`

<!-- Порождено из analysis/questions.json: python3 verify/ci/gates/coverage/check_package_questions.py --emit. Не править руками. -->

Каталог **предусмотренных** запросов §172 и того, чем каждый проверен (DECISION-0190). Карточка не означает положительного ответа по делу: ответ даёт только evaluation-документ с доказательством. Отсутствие карточки означает «не описано каталогом», а не «право молчит».

## Предмет главы, общий и максимальный сроки, их изменение и новый срок от признания (ст. 10.1–10.4)

Единицы источника: PICC_ART10_1_EN, PICC_ART10_1_RU, PICC_ART10_2_EN, PICC_ART10_2_RU, PICC_ART10_3_EN, PICC_ART10_3_RU, PICC_ART10_4_EN, PICC_ART10_4_RU.

| id | вопрос | форма | цель | шаблон | ветви | проверено |
|---|---|---|---|---|---|---|
| `chapter-does-not-govern-notice-time` | Регулирует ли глава срок на извещение или иное действие (ст. 10.1 п. 2)? | truth | `chapter_does_not_govern_notice_time(r: Right)` | `evaluate truth(chapter_does_not_govern_notice_time(r: <r>));` | — | тестов 1 |
| `general-period-expires-on` | Каким днём истекает общий срок исковой давности (ст. 10.2 п. 1)? | truth | `general_period_expires_on(r: Right, day: Date)` | `evaluate truth(general_period_expires_on(r: <r>, day: <day>));` | — | тестов 1 |
| `limitation-governed` | Ограничено ли осуществление права сроком исковой давности (ст. 10.1 п. 1)? | truth | `limitation_governed(r: Right)` | `evaluate truth(limitation_governed(r: <r>));` | — | тестов 1 |
| `maximum-period-does-not-restart` | Начинается ли максимальный срок заново после признания долга (ст. 10.4 п. 2)? | truth | `maximum_period_does_not_restart(r: Right)` | `evaluate truth(maximum_period_does_not_restart(r: <r>));` | — | тестов 1 |
| `maximum-period-expires-on` | Каким днём истекает максимальный срок исковой давности (ст. 10.2 п. 2)? | truth | `maximum_period_expires_on(r: Right, day: Date)` | `evaluate truth(maximum_period_expires_on(r: <r>, day: <day>));` | — | тестов 1 |
| `modification-effective` | Имеет ли силу изменение сроков сторонами (ст. 10.3)? | truth | `modification_effective(r: Right)` | `evaluate truth(modification_effective(r: <r>));` | Article 10.3(a). The parties may not shorten the general limitation period to less than one year (`GeneralPeriodFloorOfOneYear`); Article 10.3(c). The parties may not extend the maximum limitation period to more than fifteen years (`MaximumPeriodCeilingOfFifteenYears`); Article 10.3(b). The parties may not shorten the maximum limitation period to less than four years (`MaximumPeriodFloorOfFourYears`); Article 10.3. The parties may modify the limitation periods (`PartiesMayModifyPeriods`) | тестов 1 |
| `new-general-period-expires-on` | Каким днём истекает новый общий срок после признания долга (ст. 10.4 п. 1)? | truth | `new_general_period_expires_on(r: Right, day: Date)` | `evaluate truth(new_general_period_expires_on(r: <r>, day: <day>));` | — | тестов 1 |

- **Не отвечает:** Какая императивная норма применимого права устанавливает свой срок давности? — источник отсылает вовне (PICC_ART10_1_EN). ЭТО НЕ ПРАВО ГОСУДАРСТВА. Принципы применяются, когда стороны о них договорились, либо когда суд или арбитраж берёт их как общие принципы права; императивные нормы применимого права они не заменяют (ст. 1.4 хаба `unidroit.picc`).
- **Не отвечает:** Что отвечает Конвенция ООН 1980 года об исковой давности? — источник отсылает вовне (PICC_ART10_2_EN). У КОНВЕНЦИИ ООН 1980 ГОДА ЭТОЙ ГЛАВЫ НЕТ ВОВСЕ: исковая давность вынесена за её предмет и живёт отдельной Нью-Йоркской конвенцией 1974 года. Моста к `intl.uncitral.cisg*` здесь нет по существу, а не по недоделке.
- **Не отвечает:** Какие дни считаются при исчислении срока и есть ли нерабочие? — нужны данные, которые приносит дело (PICC_ART10_2_EN). СЧЁТ ИДЁТ СО СЛЕДУЮЩЕГО ДНЯ, И ЭТО СКАЗАНО ТЕКСТОМ: «beginning on the day after the day…» обеих частей статьи 10.2. Политика §86 пакета — `start_count next_day`, и потому трёхлетний срок от 10 марта 2020 года истекает 11 марта 2023 года, а не 10-го. Календаря рабочих дней у Принципов нет: сроки календарные.
- **Не отвечает:** Каковы согласованные сторонами сроки в годах? — нужны данные, которые приносит дело (PICC_ART10_3_EN). ТРИ ГРАНИЦЫ ИЗМЕНЕНИЯ СРОКОВ (ст. 10.3) ПРЕДЪЯВЛЯЮТСЯ ФАКТАМИ ДЕЛА: сокращён ли общий срок менее чем до года, максимальный — менее чем до четырёх лет, продлён ли он более чем до пятнадцати. Сами числа сравнения модель не считает, потому что согласованные сроки приходят данными.
- **Не отвечает:** Каков официальный текст статьи главы 10? — источник отсылает вовне (PICC_ART10_1_EN, PICC_ART10_1_RU). РУССКИЙ ТЕКСТ — ПАРНЫЙ UNOFFICIAL ЯКОРЬ: официальные языки инструмента английский и французский; первичный якорь §194 — английский black-letter текст.

## Приостановление течения срока и последствия его истечения (ст. 10.5–10.11)

Единицы источника: PICC_ART10_10_EN, PICC_ART10_10_RU, PICC_ART10_11_EN, PICC_ART10_11_RU, PICC_ART10_5_EN, PICC_ART10_5_RU, PICC_ART10_6_EN, PICC_ART10_6_RU, PICC_ART10_7_EN, PICC_ART10_7_RU, PICC_ART10_8_EN, PICC_ART10_8_RU, PICC_ART10_9_EN, PICC_ART10_9_RU.

| id | вопрос | форма | цель | шаблон | ветви | проверено |
|---|---|---|---|---|---|---|
| `arbitral-proceedings-deemed-commenced` | С какого дня считается начатым арбитражное разбирательство (ст. 10.6 п. 1)? | truth | `arbitral_proceedings_deemed_commenced(r: Right)` | `evaluate truth(arbitral_proceedings_deemed_commenced(r: <r>));` | — | тестов 1 |
| `defence-still-available` | Можно ли ссылаться на право как на возражение после истечения срока (ст. 10.9 п. 3)? | truth | `defence_still_available(r: Right)` | `evaluate truth(defence_still_available(r: <r>));` | — | тестов 1 |
| `exercise-barred` | Преграждено ли осуществление права истечением срока (ст. 10.9 п. 2)? | truth | `exercise_barred(r: Right)` | `evaluate truth(exercise_barred(r: <r>));` | — | тестов 1 |
| `general-period-not-expiring-before` | Ранее какого дня общий срок не может истечь при препятствии (ст. 10.8)? | truth | `general_period_not_expiring_before(r: Right, day: Date)` | `evaluate truth(general_period_not_expiring_before(r: <r>, day: <day>));` | — | тестов 1 |
| `limitation-suspended` | Приостановлено ли течение срока исковой давности (ст. 10.5–10.8)? | truth | `limitation_suspended(r: Right)` | `evaluate truth(limitation_suspended(r: <r>));` | Article 10.7. Articles 10.5 and 10.6 apply with appropriate modifications to proceedings whereby the parties request a third person to assist them in reaching an amicable settlement (`SuspensionByAmicableSettlementProceedings`); Article 10.6(1). The running of the limitation period is suspended when the obligee performs an act recognised by the law of the arbitral tribunal as asserting its right (`SuspensionByArbitralAct`); Article 10.5(1)(c). The running of the limitation period is suspended where the obligee has asserted its rights in proceedings for dissolution of the obligor (`SuspensionByDissolutionClaim`); Article 10.8(2). Where the impediment consists of the incapacity or death of a party, suspension ceases when a representative or successor has been appointed; the additional one-year period applies accordingly (`SuspensionByIncapacityEndsOnAppointment`); Article 10.5(1)(b). The running of the limitation period is suspended where the obligee has asserted its rights in the insolvency proceedings (`SuspensionByInsolvencyClaim`); Article 10.5(1)(a). The running of the limitation period is suspended when the obligee performs an act recognised by the law of the court as asserting its right (`SuspensionByJudicialAct`) | тестов 1 |
| `no-restitution-for-expired-right` | Можно ли вернуть исполненное по задавненному обязательству (ст. 10.11)? | truth | `no_restitution_for_expired_right(r: Right)` | `evaluate truth(no_restitution_for_expired_right(r: <r>));` | — | тестов 1 |
| `right-not-extinguished` | Прекращается ли право истечением срока исковой давности (ст. 10.9 п. 1)? | truth | `right_not_extinguished(r: Right)` | `evaluate truth(right_not_extinguished(r: <r>));` | — | тестов 1 |
| `set-off-still-available` | Можно ли осуществить зачёт до заявления об истечении срока (ст. 10.10)? | truth | `set_off_still_available(r: Right)` | `evaluate truth(set_off_still_available(r: <r>));` | — | тестов 1 |

- **Не отвечает:** Сколько дней срока осталось после окончания приостановления? — нужны данные, которые приносит дело (PICC_ART10_5_EN, PICC_ART10_8_EN). ПРИОСТАНОВЛЕНИЕ ЗДЕСЬ — ФАКТ ДЕЛА, А НЕ РАСЧЁТ: модель отвечает, приостановлено ли течение срока и ранее какого дня он не может истечь, но не пересчитывает остаток срока по дням приостановления — источник такого правила не даёт, а придумывать арифметику за него нельзя.
- **Не отвечает:** Признаёт ли право суда или арбитража это действие заявлением права? — источник отсылает вовне (PICC_ART10_5_EN, PICC_ART10_6_EN). ЧТО ПРИЗНАЁТСЯ ЗАЯВЛЕНИЕМ ПРАВА В РАЗБИРАТЕЛЬСТВЕ, РЕШАЕТ ПРАВО СУДА ИЛИ АРБИТРАЖА (ст. 10.5, 10.6): это прямая отсылка вовне, и в модель она входит фактом дела.

## Итог

Карточек 15, границ 7, внутренних звеньев 0; выводимых предикатов в CLIR 15, норм 0 — поверхность закрыта в обе стороны. Причины по конкретному делу берутся не из каталога, а из issues и why_not ответа.
