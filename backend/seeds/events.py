"""Events seeding data"""

from JDISCTF.models import Event


def get_records():
    """Get the records to add to the database"""
    return [
        Event(name='Qualifications CS Games 2019', teams=True, id=0, front_page="""
# Qualifications CS Games 2019

Les **Computer Science Games**, c'est une compétition inter-universitaire et multi-disciplinaire pour les étudiant-e-s en informatique (peu importe la faculté). Du 13 au 16 mars, une trentaine d'équipes d'une vingtaine d'universités en Amérique du Nord se rencontreront, socialiseront et, bien sûr, compétitionneront dans diverses branches de l'informatique telles que le développement Web, les bases de données, le développement mobile, la sécurité informatique, et bien d'autres!

JDIS sélectionnera **20** participant-e-s pour former la délégation sherbrookoise. C'est pourquoi nous organisons ces qualifications, afin de déterminer qui a le "best fit" pour nous permettre de bien représenter l'UdeS dans la communauté.

Info CS Games: [http://2020.csgames.org](http://2020.csgames.org)


        """),
        Event(name='JDIS Games 2019', teams=True, front_page='**JDISGames 2019**'),
        Event(name='Pico CTF 2019', teams=False, front_page='**PicoCTF 2019**'),
        Event(name='United CTF 2019', teams=False, front_page='**UnitedCTF 2019**')
    ]


FILTER_ARGS = {'name'}
