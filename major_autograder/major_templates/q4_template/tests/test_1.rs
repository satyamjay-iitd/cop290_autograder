mod hidden_tests {
    use std::{cell::RefCell, rc::Rc};

    use template::DoublyLinkedList;

    #[test]
    fn test_single() {
        {
            let n = Rc::new(RefCell::new(DoublyLinkedList {
                data: 100,
                next: None,
                prev: None,
            }));
            DoublyLinkedList::insert_after(&n, 200);

            assert!(n.borrow().prev.is_none());
            assert!(n.borrow().next.is_some());
            assert_eq!(2, Rc::strong_count(&n));

            DoublyLinkedList::delete(&n);
            assert_eq!(1, Rc::strong_count(&n));
        }
    }

    #[test]
    fn test_multiple_nodes() {
        let n1 = Rc::new(RefCell::new(DoublyLinkedList {
            data: 1,
            next: None,
            prev: None,
        }));

        DoublyLinkedList::insert_after(&n1, 2);
        let n2 = n1.borrow().next.clone().unwrap();

        DoublyLinkedList::insert_after(&n2, 3);
        let n3 = n2.borrow().next.clone().unwrap();

        // Check structure: n1 <-> n2 <-> n3
        assert_eq!(n1.borrow().next.as_ref().unwrap().borrow().data, 2);
        assert_eq!(n2.borrow().prev.as_ref().unwrap().borrow().data, 1);
        assert_eq!(n2.borrow().next.as_ref().unwrap().borrow().data, 3);
        assert_eq!(n3.borrow().prev.as_ref().unwrap().borrow().data, 2);

        // Delete n2
        DoublyLinkedList::delete(&n2);

        // Now: n1 <-> n3
        assert_eq!(n1.borrow().next.as_ref().unwrap().borrow().data, 3);
        assert_eq!(n3.borrow().prev.as_ref().unwrap().borrow().data, 1);
    }
}
