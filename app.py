from aiohttp import web
from app import get_moderator_chain


async def moderate_text(request):
    try:
        data = await request.json()

        # Валидация входных данных
        if 'text' not in data:
            raise ValueError("The 'text' parameter is required.")
        text = data['text']
        if not isinstance(text, str):
            raise ValueError("The 'text' parameter must be a string.")
        if len(text) > 4096:
            raise ValueError("The 'text' parameter must not exceed 4096 characters.")

        # Получаем цепочку модераторов из init
        moderator_chain = get_moderator_chain()

        results = []
        await moderator_chain.handle(text, results)

        return web.json_response({
            'success': True,
            'data': results
        })
    except ValueError as ve:
        return web.json_response({
            'success': False,
            'error': str(ve)
        }, status=400)
    except Exception as e:
        return web.json_response({
            'success': False,
            'error': str(e)
        }, status=500)


async def init_app():
    app = web.Application()
    app.router.add_post('/moderate', moderate_text)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=5050)
