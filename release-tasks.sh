echo "Running Release Tasks"

echo "Running Migrations"
python underwearshop/manage.py migrate

echo "Creating a superuser"
python underwearshop/manage.py createsuperuser --noinput

echo "Done"
