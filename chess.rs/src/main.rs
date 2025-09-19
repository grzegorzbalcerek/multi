pub mod color;

use crate::color::Color;

fn main() {
    println!("Hello, world! {:?}", Color::White);
    println!("Hello, world! {:?}", Color::Black.other());
}
