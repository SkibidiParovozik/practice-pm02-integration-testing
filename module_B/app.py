from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DB_PATH = 'zapav.db'
IMAGE_FOLDER = 'static/images'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Category').fetchall()
    conn.close()
    return jsonify([dict(cat) for cat in categories])


@app.route('/api/cars', methods=['GET'])
def get_cars():
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM Car ORDER BY brand, model').fetchall()
    conn.close()
    return jsonify([dict(car) for car in cars])


@app.route('/api/parts', methods=['GET'])
def get_parts():
    category_id = request.args.get('category_id')
    car_id = request.args.get('car_id')

    conn = get_db_connection()
    parts = []

    try:
        if category_id:
            # Фильтрация по категории
            query = '''
                SELECT p.*, m.name as manufacturer_name, c.name as category_name
                FROM Part p
                LEFT JOIN Manufacturer m ON p.manufacturer_id = m.id
                LEFT JOIN Category c ON p.category_id = c.id
                WHERE p.category_id = ?
            '''
            parts = conn.execute(query, (category_id,)).fetchall()
            print(f"Найдено запчастей по категории {category_id}: {len(parts)}")

        elif car_id:
            # Фильтрация по автомобилю через таблицу Part_Car
            query = '''
                SELECT p.*, m.name as manufacturer_name, 
                       GROUP_CONCAT(DISTINCT car.brand || ' ' || car.model) as compatible_cars
                FROM Part p
                JOIN Part_Car pc ON p.id = pc.part_id
                JOIN Car car ON pc.car_id = car.id
                LEFT JOIN Manufacturer m ON p.manufacturer_id = m.id
                WHERE pc.car_id = ?
                GROUP BY p.id
            '''
            parts = conn.execute(query, (car_id,)).fetchall()
            print(f"Найдено запчастей для автомобиля {car_id}: {len(parts)}")
        else:
            # Все запчасти
            query = '''
                SELECT p.*, m.name as manufacturer_name, c.name as category_name
                FROM Part p
                LEFT JOIN Manufacturer m ON p.manufacturer_id = m.id
                LEFT JOIN Category c ON p.category_id = c.id
            '''
            parts = conn.execute(query).fetchall()

    except Exception as e:
        print(f"Ошибка при получении запчастей: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify([dict(part) for part in parts])


@app.route('/api/part/<int:part_id>', methods=['GET'])
def get_part_detail(part_id):
    conn = get_db_connection()
    query = '''
        SELECT p.*, m.name as manufacturer_name, m.country, 
               c.name as category_name,
               GROUP_CONCAT(DISTINCT car.brand || ' ' || car.model) as compatible_cars
        FROM Part p
        LEFT JOIN Manufacturer m ON p.manufacturer_id = m.id
        LEFT JOIN Category c ON p.category_id = c.id
        LEFT JOIN Part_Car pc ON p.id = pc.part_id
        LEFT JOIN Car car ON pc.car_id = car.id
        WHERE p.id = ?
        GROUP BY p.id
    '''
    part = conn.execute(query, (part_id,)).fetchone()
    conn.close()

    if part is None:
        return jsonify({'error': 'Запчасть не найдена'}), 404
    return jsonify(dict(part))


@app.route('/api/search', methods=['GET'])
def search_parts():
    query = request.args.get('q', '')
    conn = get_db_connection()
    sql_query = '''
        SELECT p.*, m.name as manufacturer_name, c.name as category_name
        FROM Part p
        LEFT JOIN Manufacturer m ON p.manufacturer_id = m.id
        LEFT JOIN Category c ON p.category_id = c.id
        WHERE p.name LIKE ? OR p.article LIKE ?
        LIMIT 20
    '''
    search_param = f'%{query}%'
    parts = conn.execute(sql_query, (search_param, search_param)).fetchall()
    conn.close()
    return jsonify([dict(part) for part in parts])


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


if __name__ == '__main__':
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    app.run(debug=True, port=5000)