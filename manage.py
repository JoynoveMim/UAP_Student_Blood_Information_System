import os
import sys

# Add the parent folder (UAP_Student_Blood_Information_System) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'UAP_Student_Blood_Information_System')))

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UAP_Student_Blood_Information_System.bloodbank.settings')  # Full path to settings
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
