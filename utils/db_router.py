class MasterSlaveDBRouter(object):
    def db_for_read(self,model,**hints):
        """   读    """
        print("*****"*20)
        return "slave"

    def db_for_write(self,model,**hints):
        """   写   """
        print("====="*20)
        return "default"

    def allow_relation(self,obj1,obj2,**hints):
        """   是否运行关联操作  """
        return True