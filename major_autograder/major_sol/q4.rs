use std::cell::RefCell;
/// Tasks
/// 1. `insert_after` adds a new DoublyLinkedList node to `next` of `this`.
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
        let node = match &this.borrow().next {
            None => DoublyLinkedList {
                data,
                next: None,
                prev: Some(this.clone()),
            },
            Some(n) => DoublyLinkedList {
                data,
                next: Some(n.clone()),
                prev: Some(this.clone()),
            },
        };
        this.borrow_mut().next = Some(Rc::new(RefCell::new(node)));
    }

    pub fn delete(this: &Rc<RefCell<DoublyLinkedList>>) {
        let n = this.borrow();
        if let Some(prev) = &n.prev {
            prev.borrow_mut().next = n.next.clone();
        }
        if let Some(next) = &n.next {
            next.borrow_mut().prev = n.prev.clone();
        }
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
