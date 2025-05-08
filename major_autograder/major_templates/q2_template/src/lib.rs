use std::cell::RefCell;
use std::rc::Rc;

pub struct Node {
    pub data: i32,
    pub msgs: Rc<RefCell<String>>,
}

impl Node {
    pub fn new(data: i32, msgs: Rc<RefCell<String>>) -> Self {
        todo!()
    }
}

impl Drop for Node {
    fn drop(&mut self) {
        todo!()
    }
}

pub fn drop_in_order(mut nodes: Vec<Node>, mut order: Vec<usize>) {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_drop() {
        let s = Rc::new(RefCell::new(String::from("")));
        {
            let _ = Node::new(0, s.clone());
        }
        assert_eq!("0 created. 0 dropped. ", s.borrow().as_str());
    }

    #[test]
    fn test_drop_in_order() {
        let s = Rc::new(RefCell::new(String::from("")));
        let nodes = vec![
            Node::new(0, s.clone()),
            Node::new(1, s.clone()),
            Node::new(2, s.clone()),
        ];
        drop_in_order(nodes, vec![1, 0, 2]);
        assert_eq!(
            "0 created. 1 created. 2 created. 1 dropped. 0 dropped. 2 dropped. ",
            s.borrow().as_str()
        );
    }
}
