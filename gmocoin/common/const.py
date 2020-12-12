#!python3


class ConstMeta(type):
    '''
    クラス定義そのものに対してのsetter制御用メタクラスです。
    '''
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f'Can\'t rebind const ({name})')
        else:
            self.__setattr__(name, value)


class GMOConst(metaclass=ConstMeta):
    '''
    定数定義クラスです。
    '''
    END_POINT = 'https://api.coin.z.com/'
    END_POINT_PUBLIC = END_POINT+'public/v1/'
    END_POINT_PRIVATE = END_POINT+'private'
