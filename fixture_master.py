from datetime import datetime

from app import factories


def run_fixture():
    department_marketing = factories.DepartmentFactory(
        name="営業部",
        place="本社",
        manager="田中由紀恵",
    )
    department_supply = factories.DepartmentFactory(
        name="製造部",
        place="横須賀工場",
        manager="堀田雄一",
    )

    factories.EmployeeFactory(
        name="山本一郎",
        hired_on=datetime.fromisoformat("2010-11-01T00:00:00"),
        department=department_marketing,
        role="課長",
        residence="東京都新宿区"
    )
    factories.EmployeeFactory(
        name="渡辺二郎",
        hired_on=datetime.fromisoformat("1999-06-16T00:00:00"),
        department=department_supply,
        role="主任",
        residence="神奈川県横浜市",
    )

    factories.UserFactory(name="サトシ", last_name="ヤマダ")
    factories.UserFactory(name="Jhon", last_name="Colman")
    factories.db_session.commit()


if __name__ == '__main__':
    run_fixture()
