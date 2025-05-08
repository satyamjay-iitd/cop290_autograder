mod hidden_tests {
    use std::collections::VecDeque;

    use template::{
        AddExpr, EvalErr, Expr, InterpretErr, Interpreter, MulExpr, ParseErr, Statement,
        SymbolTable, Val, test_interpreter,
    };

    #[test]
    fn test_parse_literal() {
        let val = "142".parse::<Val>();
        assert_eq!(val, Ok(Val::Lit(142)));
    }

    #[test]
    fn test_parse_variable() {
        let val = "z".parse::<Val>();
        assert_eq!(val, Ok(Val::Var("z".to_string())));
    }

    #[test]
    fn test_parse_invalid() {
        let val = "-123".parse::<Val>();
        assert_eq!(val, Err(ParseErr));
    }

    #[test]
    fn test_eval_lit() {
        // Evaluation of a constant should be its own value
        let ctx = SymbolTable::new();
        let val = Val::Lit(142);
        let result = val.eval(&ctx);
        assert_eq!(result, Ok(142));
    }

    #[test]
    fn test_eval_var_initialized() {
        // Evaluation of a variable should be its value in the sym table
        let mut ctx = SymbolTable::new();
        ctx.insert("y".to_string(), 50);
        let val = Val::Var("y".to_string());
        let result = val.eval(&ctx);
        assert_eq!(result, Ok(50));
    }

    #[test]
    fn test_eval_var_uninitialized() {
        // Evaluation of an uninitialized variable should throw error
        let ctx = SymbolTable::new();
        let val = Val::Var("z".to_string());
        let result = val.eval(&ctx);
        assert_eq!(result, Err(EvalErr::UninitializedVar("z".to_string())));
    }

    #[test]
    fn test_parse_add_expr() {
        let exp = "100+200+300".parse::<AddExpr>();
        assert_eq!(
            exp,
            Ok(AddExpr(vec![Val::Lit(100), Val::Lit(200), Val::Lit(300)]))
        );
        let exp = "100+200+z".parse::<AddExpr>();
        assert_eq!(
            exp,
            Ok(AddExpr(vec![
                Val::Lit(100),
                Val::Lit(200),
                Val::Var("z".to_string())
            ]))
        );
    }

    #[test]
    fn test_parse_mul_expr() {
        let exp = "100*200*300".parse::<MulExpr>();
        assert_eq!(
            exp,
            Ok(MulExpr(vec![Val::Lit(100), Val::Lit(200), Val::Lit(300)]))
        );
        let exp = "100*200*z".parse::<MulExpr>();
        assert_eq!(
            exp,
            Ok(MulExpr(vec![
                Val::Lit(100),
                Val::Lit(200),
                Val::Var("z".to_string())
            ]))
        );
    }

    #[test]
    fn test_parse_invalid_expr() {
        let exp = "10*200+3000".parse::<MulExpr>();
        assert_eq!(exp, Err(ParseErr));
        let exp = "10*200+3000".parse::<AddExpr>();
        assert_eq!(exp, Err(ParseErr));
    }

    #[test]
    fn test_eval_expr_val_lit() {
        let ctx = SymbolTable::new();
        let expr = Val::Lit(500);
        assert_eq!(expr.eval(&ctx), Ok(500));
    }

    #[test]
    fn test_eval_expr_val_var() {
        let mut ctx = SymbolTable::new();
        ctx.insert("z".to_string(), 100);
        let expr = Val::Var("z".to_string());
        assert_eq!(expr.eval(&ctx), Ok(100));
    }

    #[test]
    fn test_eval_expr_add_literals() {
        let ctx = SymbolTable::new();
        let expr = AddExpr(vec![Val::Lit(100), Val::Lit(200), Val::Lit(300)]);
        assert_eq!(expr.eval(&ctx), Ok(600));
    }

    #[test]
    fn test_eval_expr_add_mixed() {
        let mut ctx = SymbolTable::new();
        ctx.insert("c".to_string(), 400);
        let expr = AddExpr(vec![
            Val::Lit(100),
            Val::Var("c".to_string()),
            Val::Lit(500),
        ]);
        assert_eq!(expr.eval(&ctx), Ok(1000));
    }

    #[test]
    fn test_eval_expr_mul_literals() {
        let ctx = SymbolTable::new();
        let expr = MulExpr(vec![Val::Lit(20), Val::Lit(30), Val::Lit(40)]);
        assert_eq!(expr.eval(&ctx), Ok(24000));
    }

    #[test]
    fn test_eval_expr_mul_mixed() {
        let mut ctx = SymbolTable::new();
        ctx.insert("t".to_string(), 50);
        let expr = MulExpr(vec![Val::Lit(20), Val::Var("t".to_string()), Val::Lit(30)]);
        assert_eq!(expr.eval(&ctx), Ok(30_000));
    }

    #[test]
    fn test_eval_expr_add_uninitialized() {
        let ctx = SymbolTable::new();
        let expr = AddExpr(vec![Val::Lit(100), Val::Var("t".to_string())]);
        assert_eq!(
            expr.eval(&ctx),
            Err(EvalErr::UninitializedVar("t".to_string()))
        );
    }

    #[test]
    fn test_eval_expr_mul_uninitialized() {
        let ctx = SymbolTable::new();
        let expr = MulExpr(vec![Val::Lit(300), Val::Var("s".to_string())]);
        assert_eq!(
            expr.eval(&ctx),
            Err(EvalErr::UninitializedVar("s".to_string()))
        );
    }

    #[test]
    fn test_parse_literal_assignment() {
        let stmt = "r=420".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "r");
    }

    #[test]
    fn test_parse_variable_assignment() {
        let stmt = "x=a".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "x");
    }

    #[test]
    fn test_parse_add_expr2() {
        let stmt = "x=1+2+3".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "x");
    }

    #[test]
    fn test_parse_mul_expr2() {
        let stmt = "x=2*3*4".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "x");
    }

    #[test]
    fn test_parse_invalid_mixed_ops() {
        let result = "x=1+2*3".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_invalid_lhs() {
        let result = "bar=1".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_invalid_rhs() {
        let result = "x=%".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_empty_expr() {
        let result = "x=".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_no_equals() {
        let result = "x420".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_execute_literal_assignment() {
        let mut ctx = SymbolTable::new();
        let stmt = Statement::new("r", Box::new(Val::Lit(100)));
        let result = stmt.execute(&mut ctx);

        assert!(result.is_ok());
        assert_eq!(ctx.get("r"), Some(&100));
    }

    #[test]
    fn test_execute_expr_assignment() {
        let mut ctx = SymbolTable::new();
        ctx.insert("x".to_string(), 20);
        ctx.insert("y".to_string(), 30);

        let expr = AddExpr(vec![
            Val::Var("x".into()),
            Val::Var("y".into()),
            Val::Lit(50),
        ]);
        let stmt = Statement::new("t", Box::new(expr));
        let result = stmt.execute(&mut ctx);
        assert!(result.is_ok());
        assert_eq!(ctx.get("t"), Some(&100));

        let expr = MulExpr(vec![
            Val::Var("x".into()),
            Val::Var("y".into()),
            Val::Lit(50),
        ]);
        let stmt = Statement::new("t", Box::new(expr));
        let result = stmt.execute(&mut ctx);
        assert!(result.is_ok());
        assert_eq!(ctx.get("t"), Some(&30_000));
    }

    #[test]
    fn test_single_step_assignment() {
        let program: VecDeque<Statement> = vec![Statement {
            lhs: "z".to_string(),
            rhs: Box::new(Val::Lit(100)),
        }]
        .into();
        let mut interpreter = Interpreter::new(program);
        let result = interpreter.step();
        assert!(result.is_ok());
        assert_eq!(result.unwrap().get("z").copied(), Some(100));
    }

    #[test]
    fn test_step_multiple_statements() {
        let program: VecDeque<Statement> = vec![
            Statement::new("z", Box::new(Val::Lit(100))),
            Statement::new("z", Box::new(AddExpr(vec![Val::Lit(300), Val::Lit(400)]))),
        ]
        .into();

        let mut interpreter = Interpreter::new(program);

        interpreter.step().unwrap();
        assert_eq!(interpreter.st.get("z").copied(), Some(100));

        interpreter.step().unwrap();
        assert_eq!(interpreter.st.get("z").copied(), Some(700));
    }

    #[test]
    fn test_step_till_end() {
        let program: VecDeque<Statement> = vec![
            Statement::new("a", Box::new(Val::Lit(100))),
            Statement::new("a", Box::new(AddExpr(vec![Val::Lit(300), Val::Lit(400)]))),
        ]
        .into();

        let final_state = Interpreter::new(program).step_till_end();
        assert!(final_state.is_ok());
        let final_state = final_state.unwrap();
        assert_eq!(final_state.get("a").copied(), Some(700));
    }

    #[test]
    fn test_uninitialized_variable_error() {
        let program: VecDeque<Statement> =
            vec![Statement::new("s", Box::new(Val::Var("t".to_string())))].into();
        let mut interpreter = Interpreter::new(program);
        let result = interpreter.step();

        assert_eq!(
            result,
            Err(InterpretErr::EvalErr(EvalErr::UninitializedVar(
                "t".to_string()
            )))
        );
    }

    #[test]
    fn test_program_already_exitted() {
        let program: VecDeque<Statement> =
            vec![Statement::new("z", Box::new(Val::Lit(100)))].into();

        let mut interpreter = Interpreter::new(program);
        interpreter.step().unwrap();
        let result = interpreter.step();
        assert_eq!(result, Err(InterpretErr::ProgramAlreadyExitted));
    }

    #[test]
    fn test_without_macro() {
        // To show off the interface
        let stmts: VecDeque<Statement> =
            vec!["a=100".parse().unwrap(), "a=132".parse().unwrap()].into();
        let interpreter = Interpreter::new(stmts);
        let final_state = interpreter.step_till_end();
        assert!(final_state.is_ok());
        let final_state = final_state.unwrap();
        assert_eq!(final_state.get("a").copied(), Some(132));

        let stmts: VecDeque<Statement> = vec!["a=20*30*50".parse().unwrap()].into();
        let mut interpreter = Interpreter::new(stmts);
        let result = interpreter.step();
        assert!(result.is_ok());
        assert_eq!(result.unwrap().get("a").copied(), Some(30_000));

        let result = interpreter.step();
        assert!(result.is_err());
    }

    #[test]
    fn test_assign() {
        test_interpreter!(
            ["a=100", "a=132", "b=12"],
            [
                ["a" => 100],
                ["a" => 132],
                ["b" => 12]
            ]
        );
    }

    #[test]
    fn test_const_arith() {
        test_interpreter!(
            ["a=20*30*50", "a=20+30+50"],
            [
                ["a" => 30_000],
                ["a" => 100]
            ]
        );
    }

    #[test]
    fn test_complex() {
        test_interpreter!(
            ["a=20", "b=30", "c=10", "a=a+b+c", "b=b*c"],
            [
                ["a" => 20],
                ["a" => 20, "b" => 30],
                ["a" => 20, "b" => 30, "c" => 10],
                ["a" => 60, "b" => 30, "c" => 10],
                ["a" => 60, "b" => 300, "c" => 10]
            ]
        );
    }
}
