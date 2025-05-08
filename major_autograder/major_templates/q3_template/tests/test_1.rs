mod hidden_tests {
    use template::List;

    #[test]
    fn test_empty_list() {
        assert_eq!(List::from(vec![]), List::Nil);
    }

    #[test]
    fn test_from() {
        assert_eq!(List::from(vec![100]), List::Cons(100, Box::new(List::Nil)));
    }

    #[test]
    fn test_from_into() {
        let v: Vec<i32> = vec![100, 200, 300];
        let v2: Vec<i32> = List::from(v.clone()).into();
        assert_eq!(v2, v);
    }
}
