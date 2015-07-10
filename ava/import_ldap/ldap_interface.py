__author__ = 'ladynerd'

from ldap3 import Server, Connection, LDAPExceptionError, SUBTREE
import sys


class ActiveDirectoryHelper:
    def __init__(self):
        pass

    PAGESIZE = 1000

    def get_connection(self, parameters):
        try:
            server = Server(parameters.server)
            ldap_conn = Connection(server, user=parameters.user_dn, password=parameters.user_pw,
                                   auto_bind=True)
            return ldap_conn

        except LDAPExceptionError as e:
            print(e.message)
            print(e.args)
            sys.exit(1)

    def search(self, parameters, filterby, attrs):

        connection = self.get_connection(parameters)

        connection.search(search_base=parameters.dump_dn, search_filter=filterby, search_scope=SUBTREE,
                          attributes=attrs, paged_size=5)

        results = connection.response

        cookie = connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']

        while cookie:
            connection.search(search_base=parameters.dump_dn, search_filter=filterby, search_scope=SUBTREE,
                              attributes=attrs, paged_size=5, paged_cookie=cookie)

            results += connection.response

            cookie = connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']

        results_json = connection.response_to_json(search_result=results)

        return results_json

    # imports the users from an LDAP instance
    @staticmethod
    def import_users(parameters):
        # specify that we only care about users
        filter_fields = '(objectclass=user)'

        # specify the fields to bring back for this user
        attributes = ['distinguishedName', 'objectGUID', 'objectSid', 'cn', 'accountExpires', 'adminCount',
                      'badPasswordTime', 'badPwdCount', 'description', 'displayName', 'isCriticalSystemObject',
                      'lastLogoff', 'lastLogon', 'lastLogonTimestamp', 'logonCount', 'logonHours', 'name',
                      'primaryGroupID', 'pwdLastSet', 'sAMAccountName', 'sAMAccountType', 'uSNChanged',
                      'uSNCreated', 'userAccountControl', 'whenChanged', 'whenCreated', 'memberOf', 'proxyAddresses']

        # return a search result for these filter_fields and attributes in JSON format
        return ActiveDirectoryHelper.search(parameters, filter_fields, attributes)

    # imports the groups from an LDAP instance
    @staticmethod
    def import_groups(parameters):
        # specify that we only care about groups
        filter_fields = '(objectclass=group)'

        # specify the fields to bring back for this group
        attributes = ['distinguishedName', 'objectGUID', 'objectSid', 'cn', 'name', 'objectCategory', 'sAMAccountName']

        # return a search result for these filter_fields and attributes in JSON format
        return ActiveDirectoryHelper.search(parameters, filter_fields, attributes)
