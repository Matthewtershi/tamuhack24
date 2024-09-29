import { cn } from "../../../lib/utils";

export const BentoGrid = ({
  className,
  children,
}: {
  className?: string;
  children?: React.ReactNode;
}) => {
  return (
    <div
      className={cn(
        "grid md:auto-rows-[18rem] grid-cols-1 md:grid-cols-3 gap-10 max-w-7xl mx-auto ",
        className
      )}
    >
      {children}
    </div>
  );
};

export const BentoGridItem = ({
  id,
  className,
  title,
  description,
  header,
  img,
  imgClassName,
}: {
  id: any;
  className?: string;
  title?: string | React.ReactNode;
  description?: string | React.ReactNode;
  header?: string;
  img?: string;
  imgClassName?: string;
}) => {
  return (
    <div
      className={cn(
        "relative rounded-xl group/bento hover:shadow-xl transition duration-200 shadow-input dark:shadow-none p-4 dark:bg-beige bg-white border-2 border-transparent justify-between flex flex-col space-y-4",
        className
      )}
    >
        <div className={`${id===2 || id===3 || id===6} && 'flex justify-center h-full`}>
            <div className="w-full h-full object-cover object-center">
                {img && (
                    <img src={img} alt={img} className='w-full h-full object-cover object-center'
                    />
                )}
            </div>
        </div>

        {header}
        <div className="group-hover/bento:translate-x-2 transition duration-200 text-darkbrown">
        <div className="font-sans font-bold mb-2 text-4xl mt-2 asdfasdfasdf">
          {title}
        </div>
        <div className="font-sans font-normal text-x1 top-0 asdfasdfasdf">
          {description}
        </div>
      </div>
    </div>
  );
};
