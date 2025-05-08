mod hidden_tests {
    use template::add_a_and_a_plus_2;

    #[test]
    fn test_add_a_and_a_plus_2() {
        let mut x = Vec::new();
        x = add_a_and_a_plus_2(x, -2);
        assert_eq!(x, [-2, 0]);
    }
}
