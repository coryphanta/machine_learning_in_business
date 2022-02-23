# Итоговый проект курса "Машинное обучение в бизнесе"


Стек:

ML: sklearn, pandas, numpy API: flask


Данные взяты с kaggle -https://www.kaggle.com/deepcontractor/aircraft-accidents-failures-hijacks-dataset

Что предсказываем: действительно ли будет авиаинцидент с жертвами


Признаки:

- Incident_Date 
- fatalities_total - всего жертв
- occupants_tottal - было на борту
- survived_total - выжившие

Преобразования признаков: OHE

Использование:

### Клонируем репозиторий и создаем образ

```
$ git clone https://github.com/coryphanta/machine_learning_in_business/tree/master/course_project.git
$ docker build -t course_project .
```

### Запуск контейнера
```
docker run -p 8180:8180 -v <полный путь к директории для журнала, напримeр /var/log>:/app/log nnn/course_project
```

### Отправляем post-запрос

с полями Incident_Date, fatalities_total, occupants_tottal, survived_total на http://localhost:8180/predict

Предупреждения: 

- f-score - 0.54, маловато, необходимо дорабатывать модель. 








