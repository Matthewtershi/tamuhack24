import React from 'react'
import { BentoGrid, BentoGridItem } from './ui/BentoGrid'
import { gridItems } from '../../assets'

const Grid = () => {
  return (
    <div className="px-10 py-10 m-20" id="process">
        <h1 className="heading text-center text-7xl asdfasdf font-extrabold mb-20 text-lightbrown ">
            INSIGHT INTO OUR {' '}
            <span className="text-darkbrown"> IMPACT </span>
        </h1>
        <section className="mt-5 mb-20 p-3" style={{ userSelect: 'none' }}>
            <BentoGrid>
                {gridItems.map((item) => (
                    <BentoGridItem
                        id={item.id}
                        key={item.id}
                        title={item.title}
                        description={item.description}
                        className={item.className}
                        img={item.image}
                        imgClassName={item.imgClassName}
                    />
                ))}
            </BentoGrid>
        </section>
    </div>
  )
}

export default Grid