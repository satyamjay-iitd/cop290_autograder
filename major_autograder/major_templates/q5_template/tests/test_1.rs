mod hidden_tests {
    use template::Sortable;

    #[test]
    fn test_i32() {
        let mut v = vec![
            Sortable { value: 200 },
            Sortable { value: 100 },
            Sortable { value: 300 },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable { value: 100 },
                Sortable { value: 200 },
                Sortable { value: 300 }
            ]
        );
    }

    #[test]
    fn test_str() {
        let mut v = vec![
            Sortable {
                value: String::from("bards"),
            },
            Sortable {
                value: String::from("bar"),
            },
            Sortable {
                value: String::from("bargo"),
            },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable {
                    value: String::from("bargo")
                },
                Sortable {
                    value: String::from("bards")
                },
                Sortable {
                    value: String::from("bar")
                }
            ]
        );
    }
}
