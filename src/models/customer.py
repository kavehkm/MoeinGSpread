# internal
from .base import BaseModel


class Customer(BaseModel):
    """Customer Model"""

    __NAME__ = 'Customer'
    __TABLE__ = 'AshkhasList'
    __PK_FIELD__ = 'ID'

    ID =                0
    CODE =              1
    PREFIX =            2
    FIRST_NAME =        3
    LAST_NAME =         4
    NAME =              5
    EMAIL =             6
    STATE =             7
    CITY =              8
    ADDRESS =           9
    POST_CODE =         10
    COMPANY =           11
    COMPANY_ADDRESS =   12
    TELS =              13
    INFO =              14
    GROUP_NAME =        15

    FIELDS = (
        ID,
        CODE,
        PREFIX,
        FIRST_NAME,
        LAST_NAME,
        NAME,
        EMAIL,
        STATE,
        CITY,
        ADDRESS,
        POST_CODE,
        COMPANY,
        COMPANY_ADDRESS,
        TELS,
        INFO,
        GROUP_NAME
    )

    def __init__(
        self, id, code, prefix, first_name, last_name, name, email, state,
        city, address, post_code, company, company_address, tels, info, group_name
    ):
        self.id = id
        self.code = code
        self.prefix = prefix
        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.email = email
        self.state = state
        self.city = city
        self.address = address
        self.post_code = post_code
        self.company = company
        self.company_address = company_address
        self.tels = tels
        self.info = info
        self.group_name = group_name

    @staticmethod
    def _sql_select():
        return """
            a.ID, a.Code, a.Prefix, a.Fname, a.LName, a.Name, a.Email, a.State, a.City,
            a.Address, a.Posti, a.Company, a.CompanyAddress, a.Tel, a.Info, g.Caption
        """

    @classmethod
    def _sql_from(cls):
        return """
            AshkhasList AS a
            LEFT OUTER JOIN GroupAshkhas AS g
            ON a.GroupID = g.ID
        """
    
    @classmethod
    def _sql_where(cls):
        return 'a.ID=?'

    @property
    def pk(self):
        return self.id

    def set_prefix(self, prefix):
        if prefix not in ['آقای', 'اقای', 'خانم']:
            return
        sql = "UPDATE AshkhasList SET Prefix=? WHERE ID=?"
        query = self.connection.execute(sql, [prefix, self.id])
        query.clear()
        return prefix

    def set_group(self, group_name):
        # find group by name
        group = None
        sql = "SELECT ID FROM GroupAshkhas WHERE Caption='{}';".format(group_name)
        query = self.connection.execute(sql)
        if query.next():
            group = query.value(0)
        query.clear()
        # if group exists update current customer
        if group is not None:
            sql = "UPDATE AshkhasList SET GroupID=? WHERE ID=?"
            self.connection.execute(sql, [group, self.id])
            query.clear()

    def set_tels(self, tels):
        # find current tels
        current_tels = []
        sql = "SELECT Tel FROM AshkhasTel WHERE IDShakhs=?"
        query = self.connection.execute(sql, [self.id])
        while query.next():
            current_tels.append(query.value(0))
        query.clear()
        # calculate new and deleted tels
        new_tels = list(set(tels) - set(current_tels))
        deleted_tels = list(set(current_tels) - set(tels))
        # check for new
        if new_tels:
            sql = "INSERT INTO AshkhasTel(IDShakhs, Caption, Tel) VALUES(?, 'تلفن', ?);"
            for tel in new_tels:
                query = self.connection.execute(sql, [self.id, tel])
            query.clear()

        if deleted_tels:
            sql = "DELETE FROM AshkhasTel WHERE IDShakhs=? AND Tel=?"
            for tel in deleted_tels:
                query = self.connection.execute(sql, [self.id, tel])
            query.clear()

    def update(self, data):
        # update prefix
        prefix = self.set_prefix(data['prefix']) or self.prefix
        # update group
        self.set_group(data['group_name'])
        # update tels
        self.set_tels(data['tels'])
        # collect fields
        name = ' '.join(list(filter(lambda s: s, [prefix, data['first_name'], data['last_name']])))
        fields = {
            'Fname': data['first_name'],
            'LName': data['last_name'],
            'Name': name,
            'Email': data['email'],
            'State': data['state'],
            'City': data['city'],
            'Address': data['address'],
            'Posti': data['post_code'],
            'Company': data['company'],
            'CompanyAddress': data['company_address'],
            'Tel': '-'.join(data['tels']),
            'Info': data['info']
        }
        params = []
        sql = "UPDATE {} SET ".format(self.__TABLE__)
        for field, value in fields.items():
            sql += "{}=?, ".format(field)
            params.append(value)
        sql = sql.rstrip(', ')
        sql += " WHERE ID=?;"
        params.append(self.id)
        query = self.connection.execute(sql, params)
        query.clear()
