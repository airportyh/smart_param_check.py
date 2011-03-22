import unittest
from smart_param_check import Mock
class TestSmartParamCheckBasic(unittest.TestCase):
    
    def setUp(self):
        def f(a, b):
            pass
        self.f = Mock(f)
    
    def test_positional(self):
        self.f(1, 2)
        self.f.assert_called_with(1, 2)
        
    def test_positional_should_fail(self):
        self.f(2, 1)
        self.assertRaises(Exception, 
            lambda: self.f.assert_called_with(1, 2))
        
    def test_keyword_args(self):
        self.f(a=1, b=2)
        self.f.assert_called_with(a=1, b=2)
        
    def test_keyword_args_should_fail(self):
        self.f(b=2, a=1)
        self.assertRaises(Exception, 
            lambda: self.f.assert_called_with(a=2, b=1))
            
    def test_positional_should_work_w_keyword(self):
        self.f(1, 2)
        self.f.assert_called_with(1, b=2)
        self.f.assert_called_with(b=2, a=1)
        self.f.assert_called_with(a=1, b=2)
    
    def test_position_w_keyword_fail(self):
        self.f(2, 1)
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(a=1, b=2))
    
    def test_keyword_should_work_w_positional(self):
        self.f(a=1, b=2)
        self.f.assert_called_with(1, 2)
        
    def test_keyword_should_work_w_positional_fail(self):
        self.f(b=1, a=2)
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1, 2))
        
    def test_should_check_required(self):
        self.assertRaises(Exception,
            lambda: self.f(1))
        self.assertRaises(Exception,
            lambda: self.f(b=2))
        self.assertRaises(Exception,
            lambda: self.f(a=1, c=3))
        
    def test_should_disallow_unexpected(self):
        self.assertRaises(Exception,
            lambda: self.f(a=1, b=2, c=3))
            
    def test_should_disallow_unexpected_positional(self):
        self.assertRaises(Exception,
            lambda: self.f(1, 2, 3))
            
class TestSmartParamCheckOptional(unittest.TestCase):
    def setUp(self):
        def f(a, b=None):
            pass
        self.f = Mock(f)
            
    def test_should_allow_omitting_optional(self):
        self.f(1)
        
    def test_should_allow_providing_optional(self):
        self.f(1, 2)
        
    def test_keywords_allow_omitting(self):
        self.f(a=1)
        
    def test_keywords_allow_providing(self):
        self.f(1, b=2)
        self.f(a=1, b=2)
        
    def test_still_check_required(self):
        self.assertRaises(Exception,
            lambda: self.f(b=2))
            
class TestSmartParamCheckVarargs(unittest.TestCase):
    def setUp(self):
        def f(a, b=None, *vargs):
            pass
        self.f = Mock(f)
        
    def test_allow_vargs(self):
        self.f(1,2,3,4)
        self.f.assert_called_with(1,2,3,4)
        
    def test_vargs_fail(self):
        self.f(1,2,3,4)
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1,2,3))
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1,2,3,4,5))
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1,2,3,5))
            
class TestSmartParamCheckKwargs(unittest.TestCase):
    def setUp(self):
        def f(a, b=None, *vargs, **kwargs):
            pass
        self.f = Mock(f)
    
    def test_allow_kwargs(self):
        self.f(a=1, b=2, c=3)
        self.f.assert_called_with(a=1, b=2, c=3)
        self.f.assert_called_with(1, 2, c=3)
        
    def test_kwargs_fail(self):
        self.f(a=1, b=2, c=3)
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1, 2, d=3))
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1, 2, c=4))
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(1, 2, c=3, d=4))
        self.assertRaises(Exception,
            lambda: self.f.assert_called_with(a=1, b=2, c=3, d=4))
    
if __name__ == '__main__':
    unittest.main()