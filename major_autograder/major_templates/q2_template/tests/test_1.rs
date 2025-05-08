mod hidden_tests {
    use std::{cell::RefCell, rc::Rc};

    #[cfg(test)]
    mod tests {
        use template::{Node, drop_in_order};

        use super::*;

        #[test]
        fn test_drop() {
            let s = Rc::new(RefCell::new(String::from("")));
            {
                let _ = Node::new(100, s.clone());
            }
            assert_eq!("100 created. 100 dropped. ", s.borrow().as_str());
        }

        #[test]
        fn test_drop_in_order() {
            let s = Rc::new(RefCell::new(String::from("")));
            let nodes = vec![
                Node::new(100, s.clone()),
                Node::new(200, s.clone()),
                Node::new(300, s.clone()),
            ];
            drop_in_order(nodes, vec![2, 0, 1]);
            assert_eq!(
                "100 created. 200 created. 300 created. 300 dropped. 100 dropped. 200 dropped. ",
                s.borrow().as_str()
            );
        }
    }
}
