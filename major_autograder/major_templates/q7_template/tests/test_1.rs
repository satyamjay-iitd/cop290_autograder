mod hidden_tests {
    use template::{Assignment, ParserError, parse};

    #[test]
    fn test_correct1() {
        let c = parse("c=142");
        assert_eq!(
            c,
            Ok(Assignment {
                name: "c",
                val: 142
            })
        );
    }

    #[test]
    fn test_correct2() {
        let c = parse("a=askdjfas");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect1() {
        let c = parse("r=");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect2() {
        let c = parse("x=142=136");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect3() {
        let c = parse("rr=142");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect4() {
        let c = parse("Z=42");
        assert_eq!(c, Err(ParserError));
    }
}
