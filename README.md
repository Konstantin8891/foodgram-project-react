# English description is below

# Кулинарный сайт

![example workflow](https://github.com/Konstantin8891/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Сайт позволяет пользователям обмениваться рецептами. Пользователь подписываться на автора рецептов, добавлять рецепты в избранное. Реализована возможность скачать список покупок для рецептов, добавленных в корзину. Для неавторизованного пользователя реализована возможность просмотра рецептов. Все модели, использованные в проекте, добавлены в админ-панель. Реализована фильтрация рецептов по тегам.

## Стек

Django 4.0

Python 3.10

PostgreSQL 12
 
DRF 3.13.1

## Запуск контейнеров

docker-compose up --build

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
    3. Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
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

### Примеры запросов к API(с полным списком запросов можете ознакомиться по uri api/docs/):

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

# Culinary site

Users can exchange recipes using this site. User can add recipes to favorites, subscribe to authors. You can download shopping list for the recipes that you add in shopping cart and filter recipes by tags. If the user is unauthorized he can view recipes. All used models were added to admin panel. 

## Stack

Django 4.0

Python 3.10

PostgreSQL 12

DRF 3.13.1

## Running containers

docker-compose up --build

sudo docker-compose exec backend python manage.py makemigrations

sudo docker-compose exec backend python manage.py migrate

sudo docker-compose exec backend python manage.py createsuperuser

sudo docker-compose exec backend python manage.py collectstatic --no-input

sudo docker-compose exec backend python manage.py load_data

## For authorized users

Main page is available.

Page of other users is available.

Page of recipe is available.

Subscription's page is available.

1. You can subscribe and unsubscribe on the recipe's page.

2. You can subscribe and unsubscribe on the author's page.

3. When you subscribe all author's recipes are added to page "Мои подписки" and when you unsubscribe they are deleted from page "Мои подписки".

Favorite's page is available.

1. You can add recipe to favorites and delete it from favorites on the recipe's page. 

2. You can add recipe to favorites and delete it from favorites on any page with the list of recipes.

Page "Shopping list" is available.

1. You can add recipe in shopping list and delete it from it.

2. You can add recipe to shopping list and delete it from it.

3. You can download file with the list of ingredients of all recipes of shopping list.

Page "Create recipe" is available.

1. You can publish you recipe.

2. You can edit your recipe.

3. You can delete your recipe

Password editing form is available.

You can logout.

## Unauthorized users

Main page is available.

Page of recipe is available.

Authorization form is available.

Password reminder form is available.

Sign up form is available.

## Admin and admin panel

All models are in admin panel.

Filtering by username and e-mail is available for the user's model.

Filtering by name, author and tags are available for the recipe's model.

Number of adding to favorites is available on the recipe's page.

Filtering by name is available for the ingredient's model.

## API

API is implemented.

### Algorithm of registration

User sends POST-request for adding new user with email, username, first_name, last_name on /api/users/ endpoint. User sends POST-request with email and password on /api/auth/token/login/ endpoint with response that includes JWT-token.

### Examples of requests

All requests are presented in /api/docs/ endpoint

1. GET Get all tags api/tags/:

    Access: all

    Response:

{
    "id": 0,
    "name": "breakfest",
    "color": "#E26C2D",
    "slug": "breakfast"
}

2. GET Get all recipes api/recipes/

    Accesss: all.
    
    Response:

{

    "count": 123,
    "next": "http://foodgram.example.org/api/recipes/?page=4",
    "previous": "http://foodgram.example.org/api/recipes/?page=2",
    "results": 

    [

    {

        "id": 0,
        "tags": 

        [

        {
            "id": 0,
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
        }

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

            {
                 "id": 0,
                 "name": "Картофель отварной",
                 "measurement_unit": "г",
                 "amount": 1
            }
            ],
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
