# Кулинарный сайт

![example workflow](https://github.com/Konstantin8891/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

http://konstantin05.ddns.net/

Сайт позволяет пользователям обмениваться рецептами. Пользователь может добавлять рецепты, подписываться на автора рецептов, добавлять рецепты в избранное. Реализована возможность скачать список покупок для рецептов, добавленных в корзину. Для неавторизованного пользователя реализована возможность просмотра рецептов. Все модели, использованные в проекте, добавлены в админ-панель. Реализована фильтрация рецептов по тегам.

## Стек

Django 4.0

Python 3.10

PostgreSQL 12

DRF

## Запуск контейнера

sudo docker-compose exec backend python manage.py makemigrations

sudo docker-compose exec backend python manage.py migrate

sudo docker-compose exec backend python manage.py createsuperuser

sudo docker-compose exec backend python manage.py collectstatic --no-input

sudo docker-compose exec backend python manage.py load_data

## Для авторизованных пользователей:

    Доступна главная страница.
    Доступна страница другого пользователя.
    Доступна страница отдельного рецепта.
    Доступна страница «Мои подписки».
    1. Можно подписаться и отписаться на странице рецепта.
    2. Можно подписаться и отписаться на странице автора.
    3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
    Доступна страница «Избранное».
    1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
    2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
    Доступна страница «Список покупок».
    1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
    2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.
    3. Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
    4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
    Доступна страница «Создать рецепт».
    1. Есть возможность опубликовать свой рецепт.
    2. Есть возможность отредактировать и сохранить изменения в своём рецепте.
    3. Есть возможность удалить свой рецепт.
    Доступна и работает форма изменения пароля.
    Доступна возможность выйти из системы (разлогиниться).

## Для неавторизованных пользователей

    Доступна главная страница.
    Доступна страница отдельного рецепта.
    Доступна и работает форма авторизации.
    Доступна и работает система восстановления пароля.
    Доступна и работает форма регистрации.

## Администратор и админ-зона

    Все модели выведены в админ-зону.
    Для модели пользователей включена фильтрация по имени и email.
    Для модели рецептов включена фильтрация по названию, автору и тегам.
    На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
    Для модели ингредиентов включена фильтрация по названию.
    
## API

Реализован API. 

Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email, username, first_name, last_name, password на конечную точку /api/users/.
Пользователь отправляет POST-запрос с параметрами email и password на конечную точку /api/auth/token/login/, в ответе на запрос ему приходит token (JWT-токен).

Пользовательские роли Аноним — может просматривать описания произведений, читать отзывы и комментарии. Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю. Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии. Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. Суперюзер Django — обладет правами администратора (admin)

Примеры запросов к API(с полным списком пользователей можете ознакомиться по uri api/docs/):

1. get Получение списка тэгов api/tags/:

    Права доступа: все.

    Ответ:

{
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
}

2. get Получение списка рецептов api/recipes/

    Права доступа: все.
    
    Ответ:

{

    "count": 123,
    "next": "http://foodgram.example.org/api/recipes/?page=4",
    "previous": "http://foodgram.example.org/api/recipes/?page=2",
    "results": 

[

{

    "id": 0,
    "tags": 

[],
"author": 
{},
"ingredients": 

            [],
            "is_favorited": true,
            "is_in_shopping_cart": true,
            "name": "string",
            "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
            "text": "string",
            "cooking_time": 1
        }
    ]

}

3. post Добавление нового рецепта api/recipes

    Запрос:

{

    "ingredients": 

[

    {
        "id": 1123,
        "amount": 10
    }

],
"tags": 

    [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1

}

    Права доступа: авторизованный пользователь

    Ответ:

{

    "id": 0,
    "tags": 

[

    {}

],
"author": 
{

    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false

},
"ingredients": 
[

        {}
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "text": "string",
    "cooking_time": 1

}

4. get Получение рецепта api/recipes/{recipe_id}/

    Права доступа: все

    Ответ:

{
    "id": 0,
    "tags": 
[
    {}
],
"author": 
{
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
},
"ingredients": 
[
        {}
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "text": "string",
    "cooking_time": 1

}

5. post Добавить рецепт в избранное api/recipes/{id}/favorite/

    Права доступа: авторизованный пользователь

    Ответ:

{

    "id": 0,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "cooking_time": 1

}

6. delete Удалить рецепт из избранного api/recipes/{id}/favorite/

Права доступа: авторизованный пользователь

7. get Получить список подписок api/users/subscriptions/

    Права доступа: авторизованный пользователь 
    
    Ответ:

{

    "count": 123,
    "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
    "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
    "results": 

[

{

    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": true,
    "recipes": 

            [],
            "recipes_count": 0
        }
    ]

}

8. post Подписаться на пользователя api/users/{id}/subscribe/

    Права доступа: авторизованный пользователь.

    Ответ:

{

    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": true,
    "recipes": 

[

        {
            "id": 0,
            "name": "string",
            "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
            "cooking_time": 1
        }
    ],
    "recipes_count": 0

}

9. delete Отписаться от пользователя api/users/{id}/subscribe/

    Права доступа: авторизованный пользователь

10. get Получить список ингредиентов api/ingredients/

    Права доступа: все

    Ответ:

[

    {
        "id": 0,
        "name": "Капуста",
        "measurement_unit": "кг"
    }

]
