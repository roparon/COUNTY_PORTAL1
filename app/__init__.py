from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from app.extensions import db, migrate, mail, security, csrf
from app.config import Config
import json

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    from app.main.views import main_bp
    from app.api.routes import api_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    from app.models.user import User, Role
    from app.models.county import County, Department
    from app.models.permit import PermitType
    from app.forms import ExtendedLoginForm, ExtendedRegisterForm
    from flask_security import hash_password

    # Handle user_registered signal
    from flask_security.signals import user_registered

    @user_registered.connect_via(app)
    def user_registered_sighandler(sender, user, confirm_token, **extra):
        default_role = Role.query.filter_by(name='citizen').first()
        if default_role and not user.roles:
            user.roles.append(default_role)
            db.session.commit()
        print(f"New user registered: {user.email} in {user.county.name if user.county else 'No County'}")

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)

    with app.app_context():
        db.create_all()
        first_time_setup()

    return app


def first_time_setup():
    from app.models.user import User, Role
    from app.models.county import County, Department
    from app.models.permit import PermitType
    from flask_security import hash_password
    import json

    # Avoid reseeding
    if User.query.filter_by(email='aaronrop40@gmail.com').first():
        return

    counties_data = [
        {'name': 'Bomet County', 'code': '036', 'description': 'Kipsisgis County'},
        {'name': 'Narok County', 'code': '033', 'description': 'Maa county'},
        {'name': 'Kericho County', 'code': '035', 'description': 'Green county'},
    ]
    created_counties = {}
    for data in counties_data:
        county = County.query.filter_by(code=data['code']).first()
        if not county:
            county = County(**data)
            db.session.add(county)
        created_counties[data['code']] = county
    db.session.commit()

    departments_data = [
        {'name': 'Trade & Commerce', 'code': 'TC'},
        {'name': 'Lands & Housing', 'code': 'LH'},
        {'name': 'Health Services', 'code': 'HS'},
        {'name': 'Environment & Water', 'code': 'EW'},
    ]
    for county in created_counties.values():
        for dept_data in departments_data:
            dept = Department.query.filter_by(code=dept_data['code'], county_id=county.id).first()
            if not dept:
                dept = Department(
                    name=dept_data['name'],
                    code=dept_data['code'],
                    county_id=county.id,
                    description=f"{dept_data['name']} department for {county.name}"
                )
                db.session.add(dept)
    db.session.commit()

    permit_types_data = [
        # Trade & Commerce
        {'name': 'Business License', 'description': 'License for operating a business within the county',
         'department_code': 'TC', 'processing_fee': 5000.00, 'processing_days': 14,
         'required_documents': ['ID Copy', 'Business Registration Certificate', 'Tax PIN Certificate', 'Location Map']},
        {'name': 'Trading License', 'description': 'License for retail and wholesale trading activities',
         'department_code': 'TC', 'processing_fee': 3000.00, 'processing_days': 10,
         'required_documents': ['ID Copy', 'Business Permit', 'Store Photo']},

        # Lands & Housing
        {'name': 'Building Permit', 'description': 'Permit for construction and building activities',
         'department_code': 'LH', 'processing_fee': 15000.00, 'processing_days': 21,
         'required_documents': ['ID Copy', 'Site Plan', 'Architectural Drawings', 'Land Title Deed']},
        {'name': 'Change of Use Permit', 'description': 'Permit to change land use classification',
         'department_code': 'LH', 'processing_fee': 8000.00, 'processing_days': 28,
         'required_documents': ['ID Copy', 'Current Title Deed', 'Survey Plan', 'Development Proposal']},

        # Health Services
        {'name': 'Food Handler License', 'description': 'License for individuals handling food commercially',
         'department_code': 'HS', 'processing_fee': 1500.00, 'processing_days': 7,
         'required_documents': ['ID Copy', 'Medical Certificate', 'Passport Photo']},
        {'name': 'Health Facility License', 'description': 'License for operating health facilities',
         'department_code': 'HS', 'processing_fee': 25000.00, 'processing_days': 30,
         'required_documents': ['ID Copy', 'Professional License', 'Facility Inspection Report', 'Equipment List']},

        # Environment & Water
        {'name': 'Water Connection Permit', 'description': 'Permit for new water connection',
         'department_code': 'EW', 'processing_fee': 5000.00, 'processing_days': 14,
         'required_documents': ['ID Copy', 'Property Ownership Proof', 'Site Plan']},
        {'name': 'Environmental Impact Assessment', 'description': 'Assessment for projects with environmental impact',
         'department_code': 'EW', 'processing_fee': 50000.00, 'processing_days': 60,
         'required_documents': ['ID Copy', 'Project Proposal', 'Environmental Study', 'Community Consent']}
    ]

    for county in created_counties.values():
        for permit in permit_types_data:
            dept = Department.query.filter_by(code=permit['department_code'], county_id=county.id).first()
            if dept:
                existing = PermitType.query.filter_by(name=permit['name'], department_id=dept.id).first()
                if not existing:
                    new_permit = PermitType(
                        name=permit['name'],
                        description=permit['description'],
                        department_id=dept.id,
                        processing_fee=permit['processing_fee'],
                        processing_days=permit['processing_days'],
                        required_documents=json.dumps(permit['required_documents'])
                    )
                    db.session.add(new_permit)
    db.session.commit()

    roles_data = [
        {'name': 'super_admin', 'description': 'Administrator role with full access'},
        {'name': 'staff', 'description': 'County staff with limited access'},
        {'name': 'citizen', 'description': 'Regular citizen with basic access'},
        {'name': 'guest', 'description': 'Guest user with minimal access'},
    ]
    for role in roles_data:
        if not Role.query.filter_by(name=role['name']).first():
            db.session.add(Role(**role))
    db.session.commit()

    super_admin_role = Role.query.filter_by(name='super_admin').first()
    admin_user = User.query.filter_by(email='aaronrop40@gmail.com').first()

    if not admin_user:
        admin_user = User(
            email='aaronrop40@gmail.com',
            first_name='Aron',
            last_name='Rop',
            password=hash_password("87654321"),
            active=True,
            county_id=created_counties['036'].id,
            roles=[super_admin_role]
        )
        db.session.add(admin_user)
    db.session.commit()

    print(f"✅ First-time database setup complete for: {admin_user.email}")
