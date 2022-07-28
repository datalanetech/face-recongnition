echo -n "Full Name: "
read name

echo -n "Employee ID: "
read id


# chmod +x new_employee.py
python36 new_employee.py "$name" "$id"
sleep 2