
#[derive(Debug)]
#[derive(PartialEq)]
pub enum Color {
    White,
    Black,
}

impl Color {
    pub fn other(&self) -> Color {
        match &self {
            Color::White => Color::Black,
            Color::Black => Color::White,
        }
    }
    pub fn first_row(&self) -> i32 {
        match &self {
            Color::White => 1,
            Color::Black => 8,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::color::Color;
    #[test]
    fn test_color_other() {
        assert_eq!(Color::Black.other(), Color::White);
        assert_eq!(Color::White.other(), Color::Black);
    }
    #[test]
    fn test_color_first_row() {
        assert_eq!(Color::Black.first_row(), 8);
        assert_eq!(Color::White.first_row(), 1);
    }
}
