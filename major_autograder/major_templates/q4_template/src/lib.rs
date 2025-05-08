use std::cell::RefCell;
/// Tasks
/// 1. `insert_after` adds a new DoublyLinkedList node to `next` of `this`. Also, `this` should
/// 	become `prev` of the new node.
/// 2. `delete` deletes `this` from `prev`'s `next` and from `next`'s `prev`.
///
use std::rc::Rc;

pub struct DoublyLinkedList {
    pub data: i32,
    pub next: Option<Rc<RefCell<DoublyLinkedList>>>,
    pub prev: Option<Rc<RefCell<DoublyLinkedList>>>,
}

impl Drop for DoublyLinkedList {
    fn drop(&mut self) {
        println!("dropping {}", self.data);
    }
}

impl DoublyLinkedList {
    pub fn insert_after(this: &Rc<RefCell<DoublyLinkedList>>, data: i32) {
        todo!()
    }

    pub fn delete(this: &Rc<RefCell<DoublyLinkedList>>) {
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_single() {
        {
            let n = Rc::new(RefCell::new(DoublyLinkedList {
                data: 1,
                next: None,
                prev: None,
            }));
            DoublyLinkedList::insert_after(&n, 2);

            assert!(n.borrow().prev.is_none());
            assert!(n.borrow().next.is_some());
            assert_eq!(2, Rc::strong_count(&n));

            DoublyLinkedList::delete(&n);
            assert_eq!(1, Rc::strong_count(&n));
        }
    }
}
