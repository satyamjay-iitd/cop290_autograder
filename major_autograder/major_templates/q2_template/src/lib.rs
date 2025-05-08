/// Tasks
/// 1. Fix `enum List` so that the compiler can know its size.
/// 2. Implement `From` and `Into` for `List` to pass tests.
///
use std::convert::From;

#[derive(PartialEq, Debug)]
pub enum List {
    Cons(i32, Box<List>), // Task 1
    Nil,
}

impl From<Vec<i32>> for List {
    fn from(mut v: Vec<i32>) -> Self {
        if v.len() == 0 {
            List::Nil
        } else {
            List::Cons(v.remove(0), Box::new(List::from(v)))
        }
    }
}

impl Into<Vec<i32>> for List {
    fn into(mut self) -> Vec<i32> {
        let mut v = vec![];
        while self != List::Nil {
            match self {
                List::Nil => {}
                List::Cons(x, l) => {
                    v.push(x);
                    self = *l;
                }
            }
        }
        v
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_list() {
        assert_eq!(List::from(vec![]), List::Nil);
    }

    #[test]
    fn test_from() {
        assert_eq!(List::from(vec![1]), List::Cons(1, Box::new(List::Nil)));
    }

    #[test]
    fn test_from_into() {
        let v: Vec<i32> = vec![1, 2];
        let v2: Vec<i32> = List::from(v.clone()).into();
        assert_eq!(v2, v);
    }
}
