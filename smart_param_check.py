import inspect

class Args(object):
    def __init__(self, kwargs, vargs):
        self.kwargs = kwargs
        self.vargs = vargs

    def keys(self):
        return self.kwargs.keys()
        
    def __eq__(one, other):
        return  one.kwargs == other.kwargs and \
                one.vargs == other.vargs
                
    def __ne__(one, other):
        return not one.__eq__(other)
                
    def __repr__(self):
        return "Args(%s, %s)" % (self.kwargs, self.vargs)
        
    @classmethod
    def combine(clz, sig, args, kwds):
        args_by_key = dict()
        extra = []
        for i in xrange(len(args)):
            try:
                argname = sig.args[i]
                args_by_key[argname] = args[i]
            except IndexError:
                extra.append(args[i])
        for key, val in kwds.items():
            if key in args_by_key:
                raise Exception('TODO')
            args_by_key[key] = val
        return Args(args_by_key, extra)
        
class Mock(object):
    def __init__(self, func):
        self.func = func
        self.sig = inspect.getargspec(self.func)
        self.required_args = self.get_required_args()
        self.named_args = self.get_named_args()
        self.call_args = []
        
    def __call__(self, *args, **kwds):
        args = self.combine_args(args, kwds)
        self.call_args.append(args)
        if not set(self.required_args).issubset(set(args.keys())):
            raise Exception('Not all required args are given')
        if self.sig.keywords is None and \
            not set(args.keys()).issubset(set(self.named_args)):
            raise Exception('Unexpected args were given')
        if len(args.vargs) > 0 and self.sig.varargs is None:
            raise Exception('Unexpected positional args were given')
        
    def get_required_args(self):
        ret = list(self.sig.args)
        if self.sig.defaults:
            for df in self.sig.defaults:
                ret.pop()
        return ret
        
    def get_named_args(self):
        return list(self.sig.args)
        
    def combine_args(self, args, kwds):
        return Args.combine(self.sig, args, kwds)
        
    def assert_called_with(self, *args, **kwds):
        args = self.combine_args(args, kwds)
        if self.call_args[0] != args:
            raise Exception('Expected call with %s but called with %s' % 
                (args, self.call_args[0]))