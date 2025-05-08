use std::fmt::Debug;
/// Interpreter for a program with the following spec:-
///
/// Syntax:-
/// Program -> [Statement]
/// Statement -> Symbol=Expr
/// Symbol -> lowercase_alphabet
/// Expr -> Val | AddExpr | MulExpr
/// Val -> u32 | Symbol
/// AddExpr -> Val + AddExpr
/// MulExpr -> Val * MulExpr
///
/// Operational Semantics:-
/// a=2      (Assign 2 to a)
/// b=a      (Assign 2 to b)
/// b=2+3+a  (Assign 7 to b)
/// b=2*3*a  (Assign 12 to b)
/// b=c      (Error:- c is not bound to a value)
///
/// Note that this is not a valid program: c=2*3+a
///
///
/// GUIDELINES:-
/// 1. Solve top to bottom, i.e solve section 1 first and section 4 last.
/// 2. Start by searching "todo", and replacing it with your solution.
/// 3. There are total 6 todos in 4 sections.
///    3.1 Section 1: 1 todos.
///    3.2 Section 2: 3 todos.
///    3.3 Section 3: 1 todos.
///    3.4 Section 4: 1 todos.
/// 4. Running all the testcases:- rustc interpreter.rs --test && ./interpreter
/// 5. Running the testcase only of a section:- rustc interpreter.rs --test && ./interpreter sec1
/// 6. Running the end_to_end test:- rustc interpreter.rs --test && ./interpreter test_end_to_end
use std::{collections::HashMap, collections::VecDeque, str::FromStr};

pub type Symbol = String;
pub type SymbolTable = HashMap<Symbol, u32>;

/////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// SECTION 1: Val /////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
#[derive(PartialEq, Eq, Debug)]
pub enum EvalErr {
    UninitializedVar(Symbol),
}

#[derive(PartialEq, Debug)]
pub struct ParseErr;

pub trait Expr: Debug {
    fn eval(&self, ctx: &SymbolTable) -> Result<u32, EvalErr>;
}

#[derive(PartialEq, Eq, Debug)]
pub enum Val {
    // Literal (Constants)
    Lit(u32),
    Var(Symbol),
}

impl Expr for Val {
    fn eval(&self, ctx: &SymbolTable) -> Result<u32, EvalErr> {
        todo!();
    }
}

impl FromStr for Val {
    type Err = ParseErr;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if let Ok(num) = s.parse::<u32>() {
            Ok(Val::Lit(num))
        } else if is_symbol(s) {
            Ok(Val::Var(s.to_string()))
        } else {
            Err(ParseErr)
        }
    }
}
#[cfg(test)]
mod test_sec1 {
    use super::*;
    #[test]
    fn test_parse_literal() {
        let val = "42".parse::<Val>();
        assert_eq!(val, Ok(Val::Lit(42)));
    }

    #[test]
    fn test_parse_variable() {
        let val = "a".parse::<Val>();
        assert_eq!(val, Ok(Val::Var("a".to_string())));
    }

    #[test]
    fn test_parse_invalid() {
        let val = "-1".parse::<Val>();
        assert_eq!(val, Err(ParseErr));
    }

    #[test]
    fn test_eval_lit() {
        // Evaluation of a constant should be its own value
        let ctx = SymbolTable::new();
        let val = Val::Lit(42);
        let result = val.eval(&ctx);
        assert_eq!(result, Ok(42));
    }

    #[test]
    fn test_eval_var_initialized() {
        // Evaluation of a variable should be its value in the sym table
        let mut ctx = SymbolTable::new();
        ctx.insert("x".to_string(), 10);
        let val = Val::Var("x".to_string());
        let result = val.eval(&ctx);
        assert_eq!(result, Ok(10));
    }

    #[test]
    fn test_eval_var_uninitialized() {
        // Evaluation of an uninitialized variable should throw error
        let ctx = SymbolTable::new();
        let val = Val::Var("y".to_string());
        let result = val.eval(&ctx);
        assert_eq!(result, Err(EvalErr::UninitializedVar("y".to_string())));
    }
}

/////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// SECTION 2: Expr ////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
#[derive(PartialEq, Eq, Debug)]
pub struct AddExpr(pub Vec<Val>);
impl Expr for AddExpr {
    fn eval(&self, ctx: &SymbolTable) -> Result<u32, EvalErr> {
        todo!();
    }
}

#[derive(PartialEq, Debug)]
pub enum AddMulParseErr {
    InvalidToken,
}
impl FromStr for AddExpr {
    type Err = ParseErr;
    fn from_str(rhs: &str) -> Result<Self, Self::Err> {
        if !rhs.contains('+') {
            return Err(ParseErr);
        }
        let tokens = rhs.split('+').map(str::trim).collect::<Vec<_>>();
        if tokens.len() < 2 {
            return Err(ParseErr);
        }
        let vals = tokens
            .into_iter()
            .map(|tok| tok.parse::<Val>())
            .collect::<Result<Vec<_>, _>>()?;
        Ok(AddExpr(vals))
    }
}

#[derive(PartialEq, Eq, Debug)]
pub struct MulExpr(pub Vec<Val>);
impl Expr for MulExpr {
    fn eval(&self, ctx: &SymbolTable) -> Result<u32, EvalErr> {
        todo!();
    }
}
impl FromStr for MulExpr {
    type Err = ParseErr;
    fn from_str(rhs: &str) -> Result<Self, Self::Err> {
        todo!();
    }
}

#[cfg(test)]
mod test_sec2 {
    use super::*;

    #[test]
    fn test_parse_add_expr() {
        let exp = "1+2+3".parse::<AddExpr>();
        assert_eq!(
            exp,
            Ok(AddExpr(vec![Val::Lit(1), Val::Lit(2), Val::Lit(3)]))
        );
        let exp = "1+2+a".parse::<AddExpr>();
        assert_eq!(
            exp,
            Ok(AddExpr(vec![
                Val::Lit(1),
                Val::Lit(2),
                Val::Var("a".to_string())
            ]))
        );
    }

    #[test]
    fn test_parse_mul_expr() {
        let exp = "1*2*3".parse::<MulExpr>();
        assert_eq!(
            exp,
            Ok(MulExpr(vec![Val::Lit(1), Val::Lit(2), Val::Lit(3)]))
        );
        let exp = "1*2*a".parse::<MulExpr>();
        assert_eq!(
            exp,
            Ok(MulExpr(vec![
                Val::Lit(1),
                Val::Lit(2),
                Val::Var("a".to_string())
            ]))
        );
    }

    #[test]
    fn test_parse_invalid_expr() {
        let exp = "1*2+3".parse::<MulExpr>();
        assert_eq!(exp, Err(ParseErr));
        let exp = "1*2+3".parse::<AddExpr>();
        assert_eq!(exp, Err(ParseErr));
    }

    #[test]
    fn test_eval_expr_val_lit() {
        let ctx = SymbolTable::new();
        let expr = Val::Lit(5);
        assert_eq!(expr.eval(&ctx), Ok(5));
    }

    #[test]
    fn test_eval_expr_val_var() {
        let mut ctx = SymbolTable::new();
        ctx.insert("a".to_string(), 3);
        let expr = Val::Var("a".to_string());
        assert_eq!(expr.eval(&ctx), Ok(3));
    }

    #[test]
    fn test_eval_expr_add_literals() {
        let ctx = SymbolTable::new();
        let expr = AddExpr(vec![Val::Lit(1), Val::Lit(2), Val::Lit(3)]);
        assert_eq!(expr.eval(&ctx), Ok(6));
    }

    #[test]
    fn test_eval_expr_add_mixed() {
        let mut ctx = SymbolTable::new();
        ctx.insert("x".to_string(), 4);
        let expr = AddExpr(vec![Val::Lit(1), Val::Var("x".to_string()), Val::Lit(5)]);
        assert_eq!(expr.eval(&ctx), Ok(10));
    }

    #[test]
    fn test_eval_expr_mul_literals() {
        let ctx = SymbolTable::new();
        let expr = MulExpr(vec![Val::Lit(2), Val::Lit(3), Val::Lit(4)]);
        assert_eq!(expr.eval(&ctx), Ok(24));
    }

    #[test]
    fn test_eval_expr_mul_mixed() {
        let mut ctx = SymbolTable::new();
        ctx.insert("y".to_string(), 5);
        let expr = MulExpr(vec![Val::Lit(2), Val::Var("y".to_string()), Val::Lit(3)]);
        assert_eq!(expr.eval(&ctx), Ok(30));
    }

    #[test]
    fn test_eval_expr_add_uninitialized() {
        let ctx = SymbolTable::new();
        let expr = AddExpr(vec![Val::Lit(1), Val::Var("z".to_string())]);
        assert_eq!(
            expr.eval(&ctx),
            Err(EvalErr::UninitializedVar("z".to_string()))
        );
    }

    #[test]
    fn test_eval_expr_mul_uninitialized() {
        let ctx = SymbolTable::new();
        let expr = MulExpr(vec![Val::Lit(3), Val::Var("k".to_string())]);
        assert_eq!(
            expr.eval(&ctx),
            Err(EvalErr::UninitializedVar("k".to_string()))
        );
    }
}

/////////////////////////////////////////////////////////////////////////////////////
//////////////////////////// SECTION 3: Statement ///////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
#[derive(Debug)]
pub struct Statement {
    pub lhs: Symbol,
    pub rhs: Box<dyn Expr>,
}

impl Statement {
    pub fn new(lhs: &str, rhs: Box<dyn Expr>) -> Self {
        Statement {
            lhs: lhs.to_string(),
            rhs,
        }
    }
    pub fn execute(self, ctx: &mut SymbolTable) -> Result<(), EvalErr> {
        todo!();
    }
}

fn is_symbol(s: &str) -> bool {
    s.len() == 1 && s.chars().all(|c| c.is_ascii_lowercase())
}

impl FromStr for Statement {
    type Err = ParseErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split('=').collect();
        if parts.len() != 2 {
            return Err(ParseErr);
        }
        let lhs = parts[0].trim();
        let rhs = parts[1].trim();

        if !is_symbol(lhs) {
            return Err(ParseErr);
        }
        if let Ok(e) = rhs.parse::<Val>() {
            return Ok(Statement::new(lhs, Box::new(e)));
        }
        if let Ok(e) = rhs.parse::<AddExpr>() {
            return Ok(Statement::new(lhs, Box::new(e)));
        }
        if let Ok(e) = rhs.parse::<MulExpr>() {
            return Ok(Statement::new(lhs, Box::new(e)));
        }
        Err(ParseErr)
    }
}

#[cfg(test)]
mod test_sec3 {
    use super::*;

    #[test]
    fn test_parse_literal_assignment() {
        let stmt = "a=42".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "a");
    }

    #[test]
    fn test_parse_variable_assignment() {
        let stmt = "b=a".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "b");
    }

    #[test]
    fn test_parse_add_expr() {
        let stmt = "c=1+2+3".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "c");
    }

    #[test]
    fn test_parse_mul_expr() {
        let stmt = "d=2*3*4".parse::<Statement>();
        assert!(stmt.is_ok());
        assert_eq!(stmt.unwrap().lhs, "d");
    }

    #[test]
    fn test_parse_invalid_mixed_ops() {
        let result = "e=1+2*3".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_invalid_lhs() {
        let result = "foo=1".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_invalid_rhs() {
        let result = "a=@".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_empty_expr() {
        let result = "a=".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_no_equals() {
        let result = "a42".parse::<Statement>();
        assert!(result.is_err());
    }

    #[test]
    fn test_execute_literal_assignment() {
        let mut ctx = SymbolTable::new();
        let stmt = Statement::new("x", Box::new(Val::Lit(10)));
        let result = stmt.execute(&mut ctx);

        assert!(result.is_ok());
        assert_eq!(ctx.get("x"), Some(&10));
    }

    #[test]
    fn test_execute_expr_assignment() {
        let mut ctx = SymbolTable::new();
        ctx.insert("a".to_string(), 2);
        ctx.insert("b".to_string(), 3);

        let expr = AddExpr(vec![
            Val::Var("a".into()),
            Val::Var("b".into()),
            Val::Lit(5),
        ]);
        let stmt = Statement::new("s", Box::new(expr));
        let result = stmt.execute(&mut ctx);
        assert!(result.is_ok());
        assert_eq!(ctx.get("s"), Some(&10));

        let expr = MulExpr(vec![
            Val::Var("a".into()),
            Val::Var("b".into()),
            Val::Lit(5),
        ]);
        let stmt = Statement::new("s", Box::new(expr));
        let result = stmt.execute(&mut ctx);
        assert!(result.is_ok());
        assert_eq!(ctx.get("s"), Some(&30));
    }
}

/////////////////////////////////////////////////////////////////////////////////////
////////////////////////// SECTION 4: Interpreter ///////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
#[derive(PartialEq, Debug)]
pub enum InterpretErr {
    ProgramAlreadyExitted,
    EvalErr(EvalErr),
}

pub struct Interpreter {
    pub stmts: VecDeque<Statement>,
    pub st: SymbolTable,
}

impl Interpreter {
    pub fn new(prog: VecDeque<Statement>) -> Interpreter {
        Interpreter {
            stmts: prog,
            st: SymbolTable::new(),
        }
    }
    pub fn step(&mut self) -> Result<&SymbolTable, InterpretErr> {
        todo!();
    }
    pub fn step_till_end(mut self) -> Result<SymbolTable, InterpretErr> {
        loop {
            match self.step() {
                Ok(_) => {}
                Err(InterpretErr::ProgramAlreadyExitted) => return Ok(self.st),
                Err(e) => return Err(e),
            }
        }
    }
}

#[cfg(test)]
mod test_sec4 {
    use super::*;

    #[test]
    fn test_single_step_assignment() {
        let program: VecDeque<Statement> = vec![Statement {
            lhs: "a".to_string(),
            rhs: Box::new(Val::Lit(1)),
        }]
        .into();
        let mut interpreter = Interpreter::new(program);
        let result = interpreter.step();
        assert!(result.is_ok());
        assert_eq!(result.unwrap().get("a").copied(), Some(1));
    }

    #[test]
    fn test_step_multiple_statements() {
        let program: VecDeque<Statement> = vec![
            Statement::new("a", Box::new(Val::Lit(1))),
            Statement::new("a", Box::new(AddExpr(vec![Val::Lit(3), Val::Lit(4)]))),
        ]
        .into();

        let mut interpreter = Interpreter::new(program);

        interpreter.step().unwrap();
        assert_eq!(interpreter.st.get("a").copied(), Some(1));

        interpreter.step().unwrap();
        assert_eq!(interpreter.st.get("a").copied(), Some(7));
    }

    #[test]
    fn test_step_till_end() {
        let program: VecDeque<Statement> = vec![
            Statement::new("a", Box::new(Val::Lit(1))),
            Statement::new("a", Box::new(AddExpr(vec![Val::Lit(3), Val::Lit(4)]))),
        ]
        .into();

        let final_state = Interpreter::new(program).step_till_end();
        assert!(final_state.is_ok());
        let final_state = final_state.unwrap();
        assert_eq!(final_state.get("a").copied(), Some(7));
    }

    #[test]
    fn test_uninitialized_variable_error() {
        let program: VecDeque<Statement> =
            vec![Statement::new("x", Box::new(Val::Var("y".to_string())))].into();
        let mut interpreter = Interpreter::new(program);
        let result = interpreter.step();

        assert_eq!(
            result,
            Err(InterpretErr::EvalErr(EvalErr::UninitializedVar(
                "y".to_string()
            )))
        );
    }

    #[test]
    fn test_program_already_exitted() {
        let program: VecDeque<Statement> = vec![Statement::new("a", Box::new(Val::Lit(1)))].into();

        let mut interpreter = Interpreter::new(program);
        interpreter.step().unwrap();
        let result = interpreter.step();
        assert_eq!(result, Err(InterpretErr::ProgramAlreadyExitted));
    }
}

/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// End-to-End Tests ////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////

// DONT READ THIS MACRO. IT IS USED FOR TESTING ONLY.
#[macro_export]
macro_rules! test_interpreter {
    ([$($stmt:expr),*], [$([$($key:expr => $val:expr),*]),*]) => {{
        let stmts: VecDeque<Statement> = vec![$($stmt.parse::<Statement>().unwrap()),*].into();
        let mut interpreter = Interpreter::new(stmts);

        let mut _step_idx = 0;
        $(
            let result = interpreter.step();
            assert!(result.is_ok(), "Step {} failed: {:?}", _step_idx, result);
            let symtab = result.unwrap();

            $(
                assert_eq!(
                    symtab.get($key).copied(),
                    Some($val),
                    "Mismatch at step {}: expected {} = {}",
                    _step_idx,
                    $key,
                    $val
                );
            )*

            _step_idx += 1;
        )*
    }};
}

#[cfg(test)]
mod test_end_to_end {
    use super::*;

    #[test]
    fn test_without_macro() {
        // Writing this test without the macro to show off the end-to-end interface.
        let stmts: VecDeque<Statement> =
            vec!["a=0".parse().unwrap(), "a=32".parse().unwrap()].into();
        let interpreter = Interpreter::new(stmts);
        let final_state = interpreter.step_till_end();
        assert!(final_state.is_ok());
        let final_state = final_state.unwrap();
        assert_eq!(final_state.get("a").copied(), Some(32));

        let stmts: VecDeque<Statement> = vec!["a=2*3*5".parse().unwrap()].into();
        let mut interpreter = Interpreter::new(stmts);
        let result = interpreter.step();
        assert!(result.is_ok());
        assert_eq!(result.unwrap().get("a").copied(), Some(30));

        let result = interpreter.step();
        assert!(result.is_err());
    }

    #[test]
    fn test_assign() {
        // There are 3 statements in the program.
        // And we test the values of each variable after a
        // statement is evaluated.
        test_interpreter!(
            ["a=0", "a=32", "b=2"],
            [
                ["a" => 0],
                ["a" => 32],
                ["a" => 32, "b" => 2]
            ]
        );
    }

    #[test]
    fn test_const_arith() {
        test_interpreter!(
            ["a=2*3*5", "a=2+3+5"],
            [
                ["a" => 30],
                ["a" => 10]
            ]
        );
    }

    #[test]
    fn test_complex() {
        test_interpreter!(
            ["a=2", "b=3", "c=0", "a=a+b+c", "b=b*c"],
            [
                ["a" => 2],
                ["a" => 2, "b" => 3],
                ["a" => 2, "b" => 3, "c" => 0],
                ["a" => 5, "b" => 3, "c" => 0],
                ["a" => 5, "b" => 0, "c" => 0]
            ]
        );
    }
}
